""" module providing socket functionality """
import socket
import sys

class Server:
    """ class representing a server """
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # welcoming socket
        self.port = 8080
        self.host = socket.gethostname()


    def init_server(self):
        """ function to initalize the welcoming socket """
        try:
            self.server_socket.bind((self.host, self.port))
        except socket.error as e:
            print(f"An error occured binding the socket: {e}")
            sys.exit()

        print(f"Server listening from {self.host} on port {self.port}...")
        self.server_socket.listen(1)  


if __name__ == "__main__":
    # set-up welcoming socket
    server = Server()
    server.init_server()

    # accept incoming connections
        