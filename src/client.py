import sys
import socket

def connect_to_server(socket_path):
    new_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        new_socket.connect(socket_path)
    except ConnectionRefusedError:
        sys.exit("Error: Connection refused server is not listening")
    except FileNotFoundError:
        sys.exit("Error: File not found, check that the server is listening and the socket path is the same")
    return new_socket

def send_request(file_path, connected_socket):
    print("sending request...")
    connected_socket.send(str.encode(file_path))

def recieve_request(connected_socket):
    print("recievieng request...")
    try:
        data = connected_socket.recv(1024)
    except ConnectionResetError:
        sys.exit("Error: Server disconnected")
    except KeyboardInterrupt:
        close_connection(connected_socket)
        sys.exit("\nYou have disconnected from the server")
    print(data.decode("utf-8"))

def handle_arguments(args):
    if len(args) == 1:
        sys.exit("Error: no arguments provided need -f file path")
    
    flags = ["-f"]
    if "-s" in args:
        flags.append("-s")

    if len(args) > 3 and len(flags) == 1 or len(args) > 5 and len(flags) == 2:
        sys.exit("Error: Too many arguments provided")
    
    for i in range(len(flags)):
        try:
            index = args.index(flags[i])
        except ValueError:
            sys.exit("Error: need " + flags[i] + " flag before file path")

        if len(args) == (index+1) or not args[(index+1)].strip():
            name_of_path = ""
            if i == 0:
                name_of_path += "file"
            else:
                name_of_path += "socket"
            sys.exit("Error: no " + name_of_path + " path provided")   
    return args

def parse_arguments(args):
    flags = ["-f"]
    if "-s" in args:
        flags.append("-s")
    parsed_values = []
    for i in range(len(flags)):
        index = args.index(flags[i])
        parsed_value = args[index + 1]
        name_of_path = ""
        if i == 0:
            name_of_path += "file"
        else:
            name_of_path += "socket"
        parsed_values.append(parsed_value)
    return parsed_values 

def close_connection(client_socket):
    client_socket.close()

def main():
    cmd_args = sys.argv
    validated_args = handle_arguments(cmd_args)
    parsed_values = parse_arguments(validated_args)
    file_path = parsed_values[0]
    if len(parsed_values) > 1:
        socket_path = parsed_values[1]
    else:
        socket_path = "/tmp/serverSocket"
    client_socket = connect_to_server(socket_path)
    print("Connected to server on socket " + socket_path)
    send_request(file_path, client_socket)
    recieve_request(client_socket)
    close_connection(client_socket)


main()