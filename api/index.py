from http.server import BaseHTTPRequestHandler

from flask import Flask, request, jsonify

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Hello Shivam, world, welcom to my python chapter1!'.encode('utf-8'))
        return
