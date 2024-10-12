import re
import socket

class Client:
    """ class representing a client """
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def init_client(self):
        """ initalize our client-server connection """
        # get uri from user
        uri = self.get_uri()

        # attempt connection with the server
        server_ip = uri[7:16]
        port = int(uri[17:21])

        try:
            self.client_socket.connect((server_ip, port))
            print("connection established!")
            self.client_socket.close()
        except socket.error as e:
            print(f"an error occured connecting to the server: {e}")

    def get_uri(self):
        """ gets the client input and returns it's validated form """
        request = "Enter a valid URI in the form of http://server ip/page or enter q to quit: "
        uri = input(request)
        while uri != "q" and not self.validate_uri(uri):
            uri = input(request)
        return uri

    def validate_uri(self, uri):
        """ validates the using regex """
        ip = r"\d{3}(.\d){3}" # nnn.n.n.n
        port = r"\d{4}" # port will always be 8080 (as of now)
        file = r"([A-Za-z].[A-Za-z])*"
        pattern = rf"http://{ip}:{port}/{file}"

        if re.fullmatch(pattern, uri):
            return True
        return False

if __name__ == "__main__":
    client = Client()
    client.init_client()
