""" module providing socket functionality """
import socket
import sys

class Server:
    """ class representing a server """
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # welcoming socket
        self.port = 8080
        self.host = socket.gethostname()
        self.default_file = "server/pages/index.html"

    def init_server(self):
        """ function to initalize the welcoming socket """
        try:
            self.server_socket.bind((self.host, self.port))
        except socket.error as e:
            sys.exit()

        self.server_socket.listen(1)

    def accept_clients(self):
        print("awaiting connections...")
        connection_socket, addr = self.server_socket.accept()
        request = connection_socket.recv(1024)
        contents = self.handle_request(request)
        connection_socket.send(contents.encode())
        connection_socket.close()
        return request


    def handle_request(self, request):
        request = request.split()
        method = request[0].decode("utf-8")
        path = request[1].decode("utf-8")

        print(method, path)
        if method == "GET":
            if path == "/":
                file_contents = open(self.default_file, "r").read()
                print(file_contents)
                response = f"HTTP/1.1 200 OK\n\n{file_contents}"
                return response
            
if __name__ == "__main__":
    # set-up welcoming socket
    server = Server()
    server.init_server()

    # accept incoming connections
    server.handle_clients()