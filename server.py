#  coding: utf-8
import socketserver
from pathlib import Path

import codes

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

LIPSUM = 'Lorem ipsum dolor sit amet'
HOST, PORT = "localhost", 8080


class MyWebServer(socketserver.BaseRequestHandler):
    __safe_path: Path = Path(__file__).joinpath('../www').resolve()
    __response: bytes = b'HTTP/1.1 '

    def handle(self):
        self.data: bytes = self.request.recv(1024).strip()
        print(f'Got a request of: {self.data}')

        # Check if HTTP method is valid
        if self.data.split()[0] != b'GET':
            self.__response += codes.RESP[405].encode()

            self.request.sendall(self.__response)
            print()

            return

        # extract the path from the request
        path_bytes = self.data.split()[1]

        self.path = Path('www' + path_bytes.decode()).resolve()

        is_dir = self.path.is_dir()
        is_file = self.path.is_file()

        ending_slash = path_bytes[-1] == b'/'[0]

        print(f'Request accessed the path {self.path}\n')

        # https://stackoverflow.com/a/34236245/15240293
        if (self.path != self.__safe_path and
                self.__safe_path not in self.path.parents):
            self.__response += codes.RESP[404].encode()

            self.request.sendall(self.__response)

            return

        if is_dir and not ending_slash:
            self.__response += (codes.RESP[301] %
                                (self.path.name + '/')).encode()

            self.request.sendall(self.__response)
            print()

            return

        self.__response += codes.RESP[200].encode()

        if is_dir:
            content = self.path.joinpath('index.html').read_bytes()
            self.__response += ((f'Content-Length:{len(content)}\r\n'
                                 'Content-Type: text/html; charset=utf-8\r\n'
                                 '\r\n').encode() +
                                content)

            self.request.sendall(self.__response)
            print()

            return

        if b'Accept: text/css' in self.data:
            content = self.path.read_bytes()
            self.__response += ((f'Content-Length:{len(content)}\r\n'
                                 'Content-Type: text/css; charset=utf-8\r\n'
                                 '\r\n').encode() +
                                content)

            self.request.sendall(self.__response)
            print()

            return

        if b'Accept: text/html' in self.data:
            content = self.path.read_bytes()
            self.__response += ((f'Content-Length:{len(content)}\r\n'
                                 'Content-Type: text/html; charset=utf-8\r\n'
                                 '\r\n').encode() +
                                content)

            self.request.sendall(self.__response)
            print()

            return

        self.__response += (f'Content-Length: {len(LIPSUM) + 2}\r\n\r\n'
                            f'{LIPSUM}\r\n').encode()

        self.request.sendall(self.__response)


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
