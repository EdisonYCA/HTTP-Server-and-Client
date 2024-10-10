""" module providing socket functionality """
import socket
import sys
import signal

class Server:
    """ class representing a server """
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # welcoming socket
        self.port = 8080
        self.host = socket.gethostname()
        self.default_file = "../pages/index.html"


    def init_server(self):
        """  initalize the welcoming socket, exit program if any issue doing so. """
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1) # accept at most 1 client
        except socket.error as e:
            # no connection established with the client yet, so we must present a server-side error.
            print(f"an issue occurred binding the socket or trying to listen for clients: \n{e}")
            sys.exit()


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
        return "/some-non-existent-path"

    def handle_clients(self):
        """ accept clients and send back server responses """
        while True:
            try:
                print("server awaiting a client...")
                connection_socket, addr = self.server_socket.accept()
                request = connection_socket.recv(1024)
                server_response = self.handle_request(request)
                connection_socket.send(server_response.encode())
                connection_socket.close()
                print("client handled")
            except Exception as e:
                print(f"An error occured: {e}")
                connection_socket.close()


    def handle_request(self, request):
        """ handle a clients request """
        request = request.decode("utf-8") # convert HTTP request from byte-stream to utf-8 str
        request = request.split() # delimit the request by whitespace
        method = request[0]
        path = request[1]

        if method == "GET":
            return self.serve_file(path)
   

    def shutdown(self, welcoming_socket):
        """ close the server by closing welcoming socket """
        print("shutting down server...")
        welcoming_socket.close()
        sys.exit()



if __name__ == "__main__":
    # set-up welcoming socket
    server = Server()
    server.init_server()

    # handle SIGINT (Ctrl + C) for graceful shutdown
    signal.signal(signal.SIGINT, server.shutdown)

    # handle incoming connections
    server.handle_clients()
