from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # This function will handle GET requests to the server
    def do_GET(self):
        file_path = '../data/B_10MB'  # Set the file path to the file you want to serve
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            self.end_headers()
            with open(file_path, 'rb') as file: # Open the file in binary mode and send it to the client
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
    # This function will handle POST requests to the server
    def do_POST(self):
        try:
            file_path = self.path.strip("/")
            content_length = int(self.headers['Content-Length'])
            file_content = self.rfile.read(content_length)
            with open(file_path, 'wb') as file: # Open the file in binary mode and write the content to it
                file.write(file_content)
            self.send_response(201)
            self.end_headers()   
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
server = HTTPServer(('172.20.10.12', 8000), SimpleHTTPRequestHandler) # replace IP with your IP
server.serve_forever()
