

# ! git clone https://github.com/chinmay0793/Context


# !pip install llama-index==0.5.6
# !pip install langchain==0.0.148
# !pip install openai==0.28



from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy   #pip install Flask-SQLAlchemy
import mysql.connector #pip install mysql-connector-    
from llama_index import SimpleDirectoryReader,GPTVectorStoreIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import os
import requests  # Import the requests library
import json.decoder



app = Flask(__name__)


# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/stagedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 

 # Initialize SQLAlchemy
db = SQLAlchemy(app)



# Define User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))

    def __repr__(self):
        return f"<User(id={self.id}, fname={self.fname})>"
    


def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit      
    chunk_size_limit = 600

    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

    index.save_to_disk('index.json')

    return index

def get_index():
    if not os.path.exists('index.json'):
        construct_index("Context")


@app.route('/ask_ai', methods=['GET', 'POST'])
def ask_ai():
    if request.is_json:
        query = request.json.get('query')
        if query:
            index = GPTVectorStoreIndex.load_from_disk('index.json')
            response = index.query(query)
            return jsonify({'response': response.response})
        else:
            return jsonify({'error': 'Query parameter not found'})
    else:
        return jsonify({'error': 'Unsupported Media Type', 'message': 'Request Content-Type must be application/json'})
    




@app.route('/test_ask_ai', methods=['GET'])
def test_ask_ai():

    # Get the query parameter from the URL, if provided
    query = request.args.get('query', '')
    
    # If the query is empty, use a default query
    if not query:
        query = 'i am feeling sad please help me'

    # Test with requests library
    url = 'http://127.0.0.1:5000/ask_ai'
    data = {'query': query}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()  # Attempt to decode JSON

        # Check if the response is valid JSON
        if isinstance(response_json, dict):
            # Retrieve fname from the database
            db.create_all()  # Create tables if they don't exist
            user = User.query.first()  # Retrieve the first user from the "users" table
            fname = user.fname if user else None

            # Personalized greeting with the retrieved first name
            greeting = f"Hi {fname}," if fname else ""        
            
            # Return a JSON object containing the query, personalized response, `fname`, and the updated query history
            return jsonify({
                'query': query,
                'response': {'response': greeting + response_json['response']},
                'fname': fname,
            })
        else:
            return jsonify({'error': 'Invalid JSON response'})
    
    except json.decoder.JSONDecodeError:
        return jsonify({'error': 'Failed to decode JSON response'})

# ... (rest of the code)



@app.route('/get_user_fname', methods=['GET'])
def get_user_fname():
    try:
        db.create_all()  # Create tables if they don't exist
        user = User.query.first()  # Retrieve the first user from the "users" table
        fname = user.fname if user else None
        
        return jsonify({'fname': fname})
    except Exception as e:
        return jsonify({'error': f'Error connecting to the database: {str(e)}'})


if __name__ == '__main__':
    os.environ["OPENAI_API_KEY"] = "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"
    get_index()
    app.run()
