import socket
import os
import sys
import time

def handle_arguments(args):
    if len(args) < 2:
        sys.exit("Error: no arguments provided")
    if len(args) > 3:
        sys.exit("Error: Too many arguments provided")
    if "-s" in args:
        try:
            index = args.index("-s")
        except ValueError:
            sys.exit("Error: need -s flag before socket path")

    
    return args

def parse_arguments(args):
    socket_path = ""
    if "-s" in args:
        index = args.index("-s")
        if (index+1) != len(args):
            socket_path = args[index + 1]
        return socket_path 

def handle_client_connection(server_socket):
    
    conn, addr = server_socket.accept()
    if conn:
        print("accepted client connection...")
    return conn

def start_server(socket_path):
 
    if socket_path:
        address_file_path = socket_path
    else:
        address_file_path = "/tmp/serverSocket"
    
    if os.path.exists(address_file_path):
        try:
            os.remove(address_file_path)  
        except PermissionError:
            sys.exit("Permission denied check path name and permissions on that directory")
        except IsADirectoryError:
            sys.exit("Trying to bind a directory! Must be file.")
    new_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    new_socket.bind(address_file_path)
    

    while(True):
        try:
            new_socket.listen(10)
            print("Server is listening on socket " + address_file_path)
            connection = handle_client_connection(new_socket)
            recieved_data = connection.recv(1024)
            decoded_data = recieved_data.decode("utf-8")
            handle_client_request(decoded_data, connection)
        except KeyboardInterrupt:
            try:
                try: 
                    connection.send(str.encode("Error: Server disconnected"))
                    connection.close()
                except BrokenPipeError:
                    os.remove(address_file_path) 
                    sys.exit("\nServer disconnected")
            except UnboundLocalError:
                os.remove(address_file_path) 
                sys.exit("\nServer disconnected")
            os.remove(address_file_path) 
            sys.exit("\nServer disconnected")
        

def file_exists(file_path):
    
    if os.path.isfile(file_path) == True:
        return True
    else:
        return False
    
def handle_client_request(file_path, connection):
    print("handling client request...")
    split_path = os.path.split(file_path)
    file_name = split_path[1]
    time.sleep(20)
    if file_exists(file_path):
        message = file_name + " exists"
        try:
            connection.send(str.encode(message))
            print(message+ "\n")
        except BrokenPipeError:
            print("Client Disconnected\n")

    else:
        message = file_name + " doesn't exists"
        try:
            connection.send(str.encode(message))
            print(message + "\n")
        except BrokenPipeError:
            print("Client Disconnected\n")


def main():
    cmd_args = sys.argv
    validated_args = handle_arguments(cmd_args)
    socket_path = parse_arguments(validated_args)
    start_server(socket_path)
main()
