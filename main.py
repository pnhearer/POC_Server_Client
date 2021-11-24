# Imports
import socket
import threading
import logging

# Constants
HEADER = 64
PORT = 5012
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "[DISCONNECTED]"


logging.basicConfig(filename='log.txt',level=logging.INFO)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(connection, address):
    logging.info(f"[NEW CONNECTION] {address} connected.")

    connected = True
    while connected:
        msg_length = connection.recv(HEADER).decode()
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(FORMAT)
            logging.info(f"[{address}] {msg}")
            if msg == DISCONNECT_MESSAGE:
                connected = False
        connection.send(f"Server received:\n\n{msg_length}\n\n".encode(FORMAT))

    connection.close()


def start():
    server.listen()
    logging.info(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        logging.info(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")


if __name__ == "__main__":
    print(f"[STARTING] server is starting\nIP_ADDR:{SERVER}")
    start()
