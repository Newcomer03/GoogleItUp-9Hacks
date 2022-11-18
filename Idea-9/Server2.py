# python -m http.server 8000 --directory ./my_dir

from http.server import HTTPServer , BaseHTTPRequestHandler

class echoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write(self.path[1:].encode())



def main():
    PORT = 8000
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, echoHandler)
    print("Server is running on the port %s" %PORT)
    server.serve_forever()

if __name__ == "__main__":
    main()
