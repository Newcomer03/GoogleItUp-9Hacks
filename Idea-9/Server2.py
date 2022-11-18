# python -m http.server 8000 --directory ./my_dir

from http.server import HTTPServer , BaseHTTPRequestHandler

tasklist = ["Task-1", "Task-2", "Task-3"]

class echoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/tasklist'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Task List</h1>'
            output += '<h3><a href="/tasklist/new">Add New Task</a></h3>'
            for task in tasklist:
                output += task
                output += '</br>'

            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Add New Task</h1>'

            output += '<form method="POST" enctype="multipart/form-data" action="/tasklist/new">'
            output += '<input name="task" type="text" placeholder="Add new task">'
            output += '<input type="submit" value="Add">'
            output += '</form>'

            output += '</body></html>'
            self.wfile.write(output.encode())

    def do_POST():
        if self.path.endswith('/new'):
            


def main():
    PORT = 9000
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, echoHandler)
    print("Server is running on the port %s" %PORT)
    server.serve_forever()

if __name__ == "__main__":
    main()
