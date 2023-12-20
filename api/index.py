from http.server import BaseHTTPRequestHandler

a = 10
b = 20
c = a + b

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(Hello Shivam, world, welcome to my python chapter1!'.encode('utf-8'))
        return
