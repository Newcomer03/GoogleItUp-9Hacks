"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging, cgi, requests

tasklist =[]

class S(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/tasklist'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        *{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        h1{
            background-color: lightblue;
            margin: 20px 20px 0px 20px;
            padding:5px 20px;
            border-radius: 7.5px;
        }

        h3{
            background-color: bisque;
            margin: 20px 40px;
            padding: 20px 40px;
            border-radius: 7.5px;
        }

        a{
            text-decoration: none;
        }

    </style>
</head>
<body>
    <div>
        <h1>ALERTS</h1>
    </div>
    <div>
        <h3>
            <a href="/tasklist/new">New Alert</a>
        """
            for task in tasklist:
                output += '</br>'
                output += task
                output += '<a href="/tasklist/%s/remove">  X</a>' % task

            output += '</h3></div></body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        *{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        h1{
            background-color: lightblue;
            margin: 20px 20px 0px 20px;
            padding:5px 20px;
            border-radius: 7.5px;
        }

        h3{
            background-color: bisque;
            margin: 20px 40px;
            padding: 20px 40px;
            border-radius: 7.5px;
        }

        a{
            text-decoration: none;
        }

        input, button{
            font-size: x-large;
            margin: 20px 40px;
            padding: 5px 15px;
        }

    </style>
</head>
<body>
"""
            output += '<h1>New Alert</h1>'

            output += '<form method="POST" enctype="multipart/form-data" action="/tasklist/new">'
            output += '<input name="task" type="text" placeholder="New Alert">'
            output += '<input type="submit" value="Add">'
            output += '</form>'

            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/remove'):
            listIDPath = self.path.split('/')[2]

            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        *{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        h1{
            background-color: lightblue;
            margin: 20px 20px 0px 20px;
            padding:5px 20px;
            border-radius: 7.5px;
        }

        h3{
            background-color: bisque;
            margin: 20px 40px;
            padding: 20px 40px;
            border-radius: 7.5px;
        }

        a{
            text-decoration: none;
        }

        input, button{
            font-size: x-large;
            margin: 20px 40px;
            padding: 5px 15px;
        }

    </style>
</head>
<body>"""
            output += '<h1>Remove Notification: %s</h1>' % listIDPath
            output += '<form method="POST" enctype="multipart/form-data" action="/tasklist/%s/remove">' % listIDPath
            output += '<input type="submit" value="Remove"></form>'
            output += '<a href="/tasklist">Cancel</a>'

            self.wfile.write(output.encode())

    def do_POST(self):
        if self.path.endswith('/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == "multipart/form-data":
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_task = fields.get('task')
                tasklist.append(new_task[0])

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/tasklist')
            self.end_headers()

            

        if self.path.endswith('/remove'):
            listIDPath = self.path.split('/')[2]
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == "multipart/form-data":
                list_item = listIDPath
                tasklist.remove(list_item)

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/tasklist')
            self.end_headers()



def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
        