# HTTP-Server-and-Client

This project is a personal, low-level implementation of a simple HTTP server and client using Python.

## Project Overview
- This project mimics HTTP/1.0 functionality, with a single supported method: `GET`. The server responds with an HTML page for every request.
- The server is designed to accept one client at a time, parse incoming HTTP requests, and return appropriate HTTP responses.
- The client sends HTTP requests to the server and handles the responses.

## Technologies
- **Programming Languages**: Python
- **Version Control**: Git/GitHub
- **Libraries**: `socket`

## How to Run the Project
There are two ways to run this program. In both cases, you need to:
1. Clone or download a local copy of the repository.
2. Ensure Python 3 is installed on your system.
3. Navigate to the `server` directory and run the server script.

### Running the Program via the Client Interface
1. Navigate to the `client` directory.
2. Run the client script to initiate a request to the server.

### Running the Program via a Web Browser
1. Open a web browser and enter `http://<server_ip>:<port>` in the URL bar.
2. Optionally, append `/file_name` to specify which file to fetch.

## Disclaimer
This HTTP implementation is limited to running on `localhost`. As such, any connection requests from external machines will be refused.
