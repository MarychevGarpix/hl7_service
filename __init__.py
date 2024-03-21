from client import run_client
from server import run_server, TCPHL7RequestHandler


if __name__ == "__main__":
    try:
        run_server()
    except Exception as e:
        TCPHL7RequestHandler.close_port()
        print(e)
        exit()

    try:
        run_client()
    except Exception as e:
        print(e)

