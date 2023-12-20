from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Hello Shivam are Sukhraj,  {c} world, welcome to my python chapter1!'.encode('utf-8'))
        a = 10
        b = 10

        c = b + a

        print(c)
        return
