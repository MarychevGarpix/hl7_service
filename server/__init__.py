import socketserver
import sys

from .tcp_hl7_handler import TCPHL7RequestHandler
from .conf import HOST, PORT, TIME_REPEAT_SENDING, SHOW_RESULT_TO_BROWSER


def run_server():
    print(START_MESSAGE)
    with socketserver.ThreadingTCPServer((HOST, PORT), TCPHL7RequestHandler) as server:
        server.serve_forever()


HELP_INFO = f'''{'---' * 50}\r\nHELP INFORMATION for HL7 messages(!):
Attention: {TCPHL7RequestHandler} is running. HL7 messages are being transmitted.
Description: When the application starts, a service starts that collects data from the application {TIME_REPEAT_SENDING} per second.
More: IVL-686: Отправка данных в систему РАИС (https://pm.garpix.com/browse/IVL-686).
* Possible your/server IP address to connect the clients that get data of application: {TCPHL7RequestHandler.get_all_ip_addresses().decode().split()}
* Kill TCP process when happened error "OSError: [Errno 98] Address already in use": `sudo fuser -k {PORT}/tcp`
* Listen for responses from TCPHL7Service ot some clients in command line: `telnet {TCPHL7RequestHandler.get_all_ip_addresses().decode().split()[0]} {PORT}`
* Only if `SHOW_RESULT_TO_BROWSER` = True ({SHOW_RESULT_TO_BROWSER}) listen for responses from TCPHL7Service ot some clients in browser: go to browser on page: http://{HOST}:{PORT}
{'---' * 50}'''

START_MESSAGE = f'''... Start running  TCP HL7 service [{HOST}] on port [{PORT}]. Python {sys.version} on {sys.platform}')
... wait for connection the clients...
Example of connection to HL7 TCP server: `telnet {HOST} {PORT}` or in a browser.
{HELP_INFO}'''
