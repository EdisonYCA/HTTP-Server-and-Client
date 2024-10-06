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
        """  initalize the welcoming socket, exit program if any issue doing so. """
        try:
            self.server_socket.bind((self.host, self.port))
        except socket.error as e:
            print(f"an issue occurred binding the welcoming socket: {e}")
            sys.exit()
        self.server_socket.listen(1) # accept at most 1 client


    def serve_file(self, path):
        """ fetch file at path, return 404 status code if file does not exist. """
        path = self.construct_path(path) # "/" will automatically fetch index.html
        response = ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                response = f"HTTP/1.1 200 OK\n\n {f.read()}"
        except FileNotFoundError:
            response = "HTTP/1.1 404 File Not Found"
        return response


    def construct_path(self, path):
        """ take the path request of client and construct it """
        if path == "/" or path == "/index":
            return self.default_file


    def handle_clients(self):
        """ accept clients and send back server responses """
        print("server awaiting a client...")
        connection_socket, addr = self.server_socket.accept()
        request = connection_socket.recv(1024)
        server_response = self.handle_request(request)
        connection_socket.send(server_response.encode())
        connection_socket.close()
        print("client handled")


    def handle_request(self, request):
        """ handle a clients request """
        request = request.decode("utf-8") # convert HTTP request from byte-stream to utf-8 str
        request = request.split() # delimit the request by whitespace
        method = request[0]
        path = request[1]

        if method == "GET":
            return self.serve_file(path)



if __name__ == "__main__":
    # set-up welcoming socket
    server = Server()
    server.init_server()

    # handle incoming connections
    server.handle_clients()
