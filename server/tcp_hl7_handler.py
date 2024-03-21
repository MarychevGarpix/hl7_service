import os
import socket
import socketserver
import time
from datetime import datetime
from subprocess import check_output

from .ack_message_mixin import ACKMessageMixin
from .conf import TIME_REPEAT_SENDING, PORT


class TCPHL7RequestHandler(socketserver.BaseRequestHandler, ACKMessageMixin):

    @staticmethod
    def get_all_ip_addresses() -> bytes:
        return check_output(['hostname', '--all-ip-addresses'])

    @staticmethod
    def close_port() -> None:
        os.system(f'sudo fuser -k {PORT}/tcp')

    def setup(self):
        print(f'{self.__class__.__name__}: The client {self.client_address} is connected successfully! Starting to send HL7 messages at {datetime.now()}\n')
        # Note: Avoid bind() exception: OSError: [Errno 48] Address already in use
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.socket.setblocking(False)

    def handle(self) -> None:
        while True:
            try:
                message = self.prepare_ack_message()
                self.request.sendall(message)
                time.sleep(TIME_REPEAT_SENDING)
            except (Exception, BrokenPipeError) as e:
                print(f"......connection failed. Reason: {e}\a")
                self.server.shutdown()
                exit()
