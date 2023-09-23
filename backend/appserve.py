import socket
from typing import Callable
import json

address = ('localhost', 12345)
buffer_size = 1024


def get_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def run_server(on_request: Callable[[str], object]):
    s = get_socket()
    s.bind(address)
    s.listen(1)

    while True:
        conn, addr = s.accept()
        print('Connected by', addr)

        data = conn.recv(buffer_size)
        print('Received', repr(data))
        print('Decoding', data.decode('utf-8'))
        response = on_request(json.loads(data.decode('utf-8')))
        json_response = json.dumps(response)
        
        print('Sending', json_response)
        print('Encoding', bytes(json_response, 'utf-8'))
        conn.send(bytes(json_response, 'utf-8'))
        conn.close()


def request_server(request: str) -> object:
    s = get_socket()
    s.connect(address)

    print('Sending', request)
    print('Encoding', bytes(json.dumps(request), 'utf-8'))
    s.send(bytes(json.dumps(request), 'utf-8'))

    data = s.recv(buffer_size)
    print('Received', repr(data))

    s.close()
    return json.loads(data.decode('utf-8'))
