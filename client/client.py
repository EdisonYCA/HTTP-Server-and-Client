import re
import socket
import sys

class Client:
    """ class representing a client """
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def init_client(self):
        """ initalize our client-server connection """
        # get uri from user
        uri = self.get_uri()

        # handle user quit
        if uri == "q":
            sys.exit()

        # destination IP and port
        server_ip = uri[7:16]
        port = int(uri[17:21])

        # assembling HTTP request
        file = uri[21:]
        http_req = ["GET", file]

        try:
            # attempt connection with server
            self.client_socket.connect((server_ip, port))
            print("connection established!")

            # connection established, send HTTP request
            self.client_socket.send(' '.join(http_req).encode())

            # retrieve server response
            file_contents = self.client_socket.recv(2048)
            file_contents = file_contents.decode("utf-8") # byte strea mto utf-8

            # display the file contents (using utf-8)
            print(f"file contents: \n{file_contents}")

            # close connection
            self.client_socket.close()
        except socket.error as e:
            print(f"an error occured connecting to the server: {e}")

    def get_uri(self):
        """ gets the client input and returns it's validated form """
        request = "Enter a valid URI in the form of http://server_ip:8080/page or enter q to quit: "
        uri = input(request)
        while uri != "q" and not self.validate_uri(uri):
            uri = input(request)
        return uri

    def validate_uri(self, uri):
        """ validates the using regex """
        ip = r"\d{3}(.\d){3}" # nnn.n.n.n
        file = r"([A-Za-z]/?)*"
        pattern = rf"http://{ip}:8080/{file}"

        if re.fullmatch(pattern, uri):
            return True
        return False

if __name__ == "__main__":
    client = Client()
    client.init_client()
