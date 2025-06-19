from socket import *      #for connections
import threading          #for multi request handling
import os                 #for file handling
import mimetypes          #figure out file type through the extension
import json               #JSON file handling
import time               #used for server uptime

with open('config.json', 'r') as config_file:   #open JSON configuration file and load it
    config = json.load(config_file)

#set constant variables, get their value from the config file
#get the value from the 'config' file. If it doesn't exist, set set the second argument as defualt
PORT = config.get("port", 6789)  
DEFAULT_PAGE = config.get("default_page", "HelloWorld.html")
MAX_REQUEST_SIZE = config.get("max_request_size", 2048)  #why 2048? it's 2KB, which is a safe middleground, prevents absue and helps in speed.
SERVER_START_TIME = time.time()  #calculates how long the server has been running, runs the moment the server starts


# guess the mime type, for unknown file types fall back to 'application/octet-stream'
# we use octet stream as if to say, "I don’t know what this file is, so treat it as a generic stream of bytes."
def get_mime_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type if mime_type else "application/octet-stream"

#structure the HTTP response
def format_response(status_code, content, content_type="text/html"):
    status_messages = {
        200: "OK",
        404: "Not Found"
    }
    response = f"HTTP/1.1 {status_code} {status_messages.get(status_code)}\r\n" # build the status line
    response += f"Content-Type: {content_type}\r\n\r\n" #append the header to the status line. '\r\n\r\n' separates response lines, omitting it would cause an 'Inavlid HTTP response' error
    return response + content #returns full response, header + body

#handle incoming requests
def handle_request(connection_socket, addr):
    try:
        request = connection_socket.recv(MAX_REQUEST_SIZE).decode() #if it receives more than the MAX_REQUEST_SIZE it will stay in the socket's buffer. .decode() converts bytes to string (UTF-8)
        headers = request.split('\n') #split the request at newlines to get the header. first line contains method + path
        
        #ignore if it's not a GET request
        if not headers or not headers[0].startswith('GET'): 
            return

        #extract the path (e.g. '/HelloWorld.html' (second index after splitting the first index of headers by spaces)
        filename = headers[0].split()[1]

        #if only '/' is specified in the request, redirect to default page
        if filename == '/':
            filename = '/' + DEFAULT_PAGE

        #if '/status' is specified in the request, direct to the status page
        elif filename == '/status':
            uptime = time.time() - SERVER_START_TIME #substracts current time by the time the server started to get the uptime

            #open the status HTML file to show results.
            with open('status.html', 'r', encoding='utf-8') as file:
                content = file.read().replace("{{uptime}}", f"{uptime:.2f}")
            response = format_response(200, content) #format the success response
            connection_socket.sendall(response.encode())  #turn the string back to bytes and send the response to the client
            return

        #check if file exists, if it does, open and read it then build a raw HTTP response
        filepath = '.' + filename
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as file:
                content = file.read()
            content_type = get_mime_type(filepath)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n".encode() + content  #we don't use format_reponse() bec it returns a string, while we're currently dealing with binary
        
        #if it does not exist, show a 404 page
        else:
            with open('404.html', 'r', encoding='utf-8') as file:
                content = file.read()
            response = format_response(404, content).encode()

        connection_socket.sendall(response)
    except Exception as e:
        print(f"Error handling request from {addr}: {e}")  # log errors
    finally:
        connection_socket.close()

    # why dont't we use the 'os.path.isfile(filepath)' method to fetch the status page and instead use an elif block?
    # because the status page isn't static, we need to calculate and inject the uptime into the HTML template
    # keep in mind, we're requesting /status not /status.html, so the 'if os.path.isfile(filepath):' would not work.
    # for context try searching 'http://ServerIP:6789/status.html' vs 'http://ServerIP:6789/status'


def start_server():
    server_socket = socket(AF_INET, SOCK_STREAM)  #get the IP address and create  TCP socket
    server_socket.bind(('', PORT))  #bind all interfaces to the port
    server_socket.listen(5)  #listen for no more than 5 connections
    print(f"Server is listening on port {PORT}...")

    while True:
        connection_socket, addr = server_socket.accept()  #created for each connection request, a dedicated socket and the clinet's address
        threading.Thread(target=handle_request, args=(connection_socket, addr)).start()  #creates a new thread for the connections and handles the request with the given arguments. .start() starts the thread and in turn the handle_request() method

#entry point
if __name__ == "__main__":
    start_server()