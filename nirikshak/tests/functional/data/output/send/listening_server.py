import json
import socket
import sys


def create_server(file_name, port):
    s = socket.socket()
    print "Socket successfully created"
    s.bind(('', port))
    s.listen(5)
    while True:
        # Establish connection with client.
        c, addr = s.accept()
        append_to_json_file(file_name, c.recv(10240))
        c.close()


def append_to_json_file(file_name, content):
    with open(file_name, "a") as output:
        json_formatted_content = json.dumps(content, indent=4,
                                            sort_keys=True,
                                            separators=(',', ': '))
        output.write(json_formatted_content)


if __name__ == '__main__':
    print(sys.argv)
    file_name, port = sys.argv[1:]
    print(file_name, port)
    create_server(file_name, int(port))
