import os  # Import the os module for file and directory operations
import socket  # Import the socket module for network communication
import subprocess # Import the subprocess module to run external commands

base = "htdocs"

# Define a function to create a PHP object from data
def phpObj(data):
    php_string = "$data = array(\n"
    for v in data:
        php_string += f"    '{v[0]}' => '{v[1]}',\n"
    php_string += ");"
    return php_string

def webserver(host, port):
    temp_file_location = ''
    parameters = ''
    
    print("Server is running on http://" + host + ":" + str(port))
    
    # Create a socket object and bind it to the specified host and port
    websocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    websocket.bind((host, port))
    websocket.listen(5) # Listen for incoming connections with a queue size of 5
    
    # Start an infinite loop to handle incoming requests
    while True:
        sample_file_location = ''
        parameters = ''

        # Accept an incoming connection and get the connection object and client address
        connection, address = websocket.accept()
        req_lines = connection.recv(4096).decode("utf-8").split("\r\n")
        path = req_lines[0].split(" ")[1]

        if 1 < len(path.split("?")):  # get request URL parameters
            path, parameters = path.split("?")

        req_type = req_lines[0].split(" ")[0]  # Get the request type (e.g., GET or POST)
        file_location = os.path.join(base, path.lstrip("/")) # Build the full file path

        # Check if the requested file exists and is within the base directory
        if os.path.exists(file_location) and os.path.commonpath([base, file_location]) == base:
            if os.path.isdir(file_location):
                if os.path.exists(os.path.join(file_location, "index.php")):
                    file_location = os.path.join(file_location, "index.php")
                elif os.path.exists(os.path.join(file_location, "index.html")):
                    file_location = os.path.join(file_location, "index.html")

            if not(os.path.isdir(file_location)):
                if file_location.endswith(".php"):
                    if req_type == "POST":
                        post_data = req_lines[req_lines.index('') + 1].split("&")
                        post_data = list(map(lambda x: [it for it in x.split("=")], post_data))
                        php_text = "<?php " + phpObj(post_data) + "\n $_POST = $data; ?> "
                        
                        # Read the existing PHP code from the file
                        with open(file_location, 'r') as php_file:
                            php_code = php_file.read()
                  
                        #creating a temporary file
                        directory_path = os.path.dirname(file_location)
                        file_name = "." + "sample" + "_" + os.path.basename(file_location)
                        file_location = os.path.join(directory_path, file_name)
                        sample_file_location = file_location

                        # Write the combined PHP code to the temporary file
                        with open(file_location, 'w') as php_file:
                            php_file.write(php_text + php_code)

                    if req_type == "GET" and parameters:
                        get_data = parameters.split("&")
                        get_data = list(map(lambda x: [it for it in x.split("=")], get_data))
                        php_text = "<?php " + phpObj(get_data) + "\n $_GET = $data; ?> "

                        # Read the existing PHP code from the file
                        with open(file_location, 'r') as php_file:
                            php_code = php_file.read()

                        directory_path = os.path.dirname(file_location)
                        file_name = "." + "sample" + "_" + os.path.basename(file_location)
                        file_location = os.path.join(directory_path, file_name)
                        sample_file_location = file_location

                        with open(file_location, 'w') as php_file:
                            php_file.write(php_text + php_code)

                    
                    # Execute the PHP script and capture the output
                    try:
                        output = subprocess.run(['php', file_location], capture_output=True, text=True, check=True)
                        response = "HTTP/1.1 200 OK\r\n\r\n" + output.stdout

                    except subprocess.CalledProcessError as e:
                        response = "HTTP/1.1 500 Internal Server Error\r\n\r\nInternal Server Error\n" + e.stderr

                    #Delete the temporary file
                    if sample_file_location:
                        try:
                            os.remove(sample_file_location)
                            print(f"File '{sample_file_location}' has been deleted.")
                        except OSError as e:
                            print(f"Error deleting file: {e}")

                # Serve non-PHP files
                else:
                    try:
                        with open(file_location, "rb") as file:
                            output = file.read()
                            response = "HTTP/1.1 200 OK\r\n\r\n" + output.decode("utf-8")

                    except Exception as e:
                        response = "HTTP/1.1 500 Internal Server Error\r\n\r\n" + str(e)
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
        else:
            response = "HTTP/1.1 403 Forbidden\r\n\r\nForbidden"

        # Send the HTTP response to the client
        connection.sendall(response.encode("utf-8"))
        connection.close()

host = "127.0.0.1"
port = 2728

#start the webserver
webserver(host, port)
