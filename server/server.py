""" module providing socket functionality """
import socket
import sys
import signal

class Server:
    """ class representing a server """
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # welcoming socket
        self.port = 8080 # assume user will always use this port
        self.host = "0.0.0.0"
        self.default_file = "../pages/index.html"
        self.status_404_file = "../pages/404.html"


    def init_server(self):
        """  initalize the welcoming socket, exit program if any issue doing so. """
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1) # accept at most 1 client
        except socket.error as e:
            # no connection established with the client yet, so we must present a server-side error.
            print(f"An issue occurred binding the socket or trying to listen for clients: \n{e}")
            return False
        return True


    def serve_file(self, path):
        """ fetch file at path, return 404 status code if file does not exist. """
        path = self.construct_path(path)
        response = ""
        f = open(path, "r", encoding="utf-8")

        if path == self.default_file:
            response = f"HTTP/1.1 200 OK\n\n {f.read()}"
        else:
            response = f"HTTP/1.1 404 File Not Found\n\n {f.read()}" # return an HTML for this
        return response


    def construct_path(self, path):
        """ take the path request of client and construct it """
        if path == "/" or path == "/index":
            return self.default_file
        return self.status_404_file


    def handle_clients(self):
        """ accept clients and send back server responses """
        print(f"Server running on {socket.gethostbyname(self.host)}:{self.port}")
        while True:
            try:
                # accept an incoming client and establish a socket with them
                connection_socket, addr = self.server_socket.accept()

                # get the clients request, generate a response, and send the response
                request = connection_socket.recv(1024)
                server_response = self.handle_request(request)
                connection_socket.send(server_response.encode())

                # close client connection and wait for next client
                connection_socket.close()
            except socket.error as e:
                print(f"An error occured: {e}")
                connection_socket.close()

            except KeyboardInterrupt:
                print("\nServer shutdown...")
                break



    def handle_request(self, request):
        """ handle a clients request """
        request = request.decode("utf-8") # convert HTTP request from byte-stream to utf-8 str
        request = request.split() # delimit the request by whitespace
        path = request[1] if request else self.status_404_file
        return self.serve_file(path)


if __name__ == "__main__":
    # set-up welcoming socket
    server = Server()
    INIT = server.init_server()

    # handle incoming connections
    if INIT:
        server.handle_clients()

    # close welcoming socket
    server.server_socket.close()
