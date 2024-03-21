from server import run_server
from server.tcp_hl7_handler import TCPHL7RequestHandler


if __name__ == '__main__':
    try:
        run_server()
    except Exception as e:
        TCPHL7RequestHandler.close_port()
        print(e)
        exit()
