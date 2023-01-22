#  coding: utf-8 
import socketserver
import os
import webbrowser

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Klyde Pausang

''' self.data returns:
        b'GET HTTP/1.1\r\n
        Host: 127.0.0.1:8080\r\n
        User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0\r\n
        Accept: image/avif,image/webp,*/*\r\n
        Accept-Language: en-US,en;q=0.5\r\n
        Accept-Encoding: gzip, deflate, br\r\n
        Connection: keep-alive\r\n
        Referer: http://127.0.0.1:8080/\r\n
        Sec-Fetch-Dest: image\r\nSec-Fetch-Mode: no-cors\r\n
        Sec-Fetch-Site: same-origin'''


class MyWebServer(socketserver.BaseRequestHandler):

    def error_code(self, code):
        if code == 404:
            self.status_code = 404
            self.message = "Not found"
        if code == 405:
            self.status_code = 405
            self.message = "Method Not Allowed"
        if code == 301:
            self.status_code = 301
            self.message = "Moved Permanently"


    def construct_response(self):
        self.response = 'HTTP/1.1 ' + str(self.status_code)+ ' ' + self.message +'\r\n'
                    

    def display(self,path):
        
        
        if '.html' in path:
            f = open(path)
            file = f.read()
            #self.request.sendall(bytearray(file.encode()))
            self.request.sendall(bytearray(f"{self.response}Content-type: text/html\r\n\r\n{file}",'utf-8'))
            f.close()

        if '.css' in path:
            f = open(path)
            file = f.read()
            #self.request.sendall(bytearray(file.encode()))
            self.request.sendall(bytearray(f"{self.response}Content-type: text/css\r\n\r\n{file}",'utf-8'))
            f.close
    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("0sK",'utf-8'))
        
        #status code
        self.status_code = 200
        self.message = "OK"
        


        #Parse data and get request status
        data_list = self.data.split()
        request_status = data_list[0]
        requested_path = data_list[1]


        #Serves only files in /www folder
        root_path = os.path.join(os.getcwd() + "/www" + requested_path)
        #print(root_path)
        print(requested_path)

        #redirect to index.html
        if (requested_path == '/' or requested_path == '/deep/'):
            root_path += 'index.html'
        
        #hacky way to do this. refactor if possible
        #code 301
        if(requested_path == "/deep"):
            root_path += '/index.html'
            self.error_code(301)
            print(self.status_code)
            

        #Check if request_status is GET
        if(request_status != 'GET'):
            self.error_code(405)
            print(self.status_code)
        else:
            
        
            #handle path doesnt exist
            if (not os.path.exists(root_path)):
                self.error_code(404)
                self.construct_response()
                print(self.response)

            else:

                self.construct_response()
                self.display(root_path)#opens html
                
                
                print(self.response)

    
            



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
