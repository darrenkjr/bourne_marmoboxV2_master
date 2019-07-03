import socketserver
import http.server
import logging
import cgi


class ServerHandler(http.server.SimpleHTTPRequestHandler):


    def server_start(self):
        PORT = 8000
        Handler = ServerHandler
        httpd = socketserver.TCPServer(("", PORT), Handler)

        print("serving at port", PORT)
        httpd.serve_forever()



    def do_GET(self):
        logging.error(self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.error(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        for item in form.list:
            logging.error(item)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

        with open("data.txt", "w") as file:
            for key in form.keys():
                file.write(str(form.getvalue(str(key))) + ",")
