import socket
import sys

# TODO: from server.conf import HOST, PORT
HOST: str = "0.0.0.0"
PORT: int = 9000


def run_client():
    print(START_MESSAGE)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            # s.sendall(b"Hello TCP HL7 server")
        except (ConnectionRefusedError, KeyboardInterrupt, Exception) as e:
            print(f'Connection to TCP HL7 service failed. Reason: {e}')
            exit()

        while True:
            try:
                print(s.recv(1024).decode('utf-8'))
            except (ConnectionRefusedError, KeyboardInterrupt, Exception) as e:
                print(f'Connection to TCP HL7 service failed. Reason: {e}')
                exit()


START_MESSAGE = f'''... Start connecting to  TCP HL7 server [{HOST}] on port [{PORT}]. Python {sys.version} on {sys.platform}')
... wait for responses of HL7 messages from server'''

