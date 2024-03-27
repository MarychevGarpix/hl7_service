import random

from hl7apy.core import Message, Segment

from mock_data import STRUCTURE_DATA
from server.conf import SHOW_RESULT_TO_BROWSER


class ACKMessageMixin:
    """
    Info about ACK messages:
    Rules formation: https://hl7-definition.caristix.com/v2/HL7v2.6/TriggerEvents/ACK
    Documentation ACK: https://repository.immregistries.org/files/resources/5835adc2add61/guidance_for_hl7_acknowledgement_messages_to_support_interoperability_.pdf
    About ACK messages: https://www.interfaceware.com/hl7-ack
    """
    NAME = 'ACK'
    HTML_HEADER: bytes = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.encode('utf-8')

    def prepare_message(self) -> bytes:
        try:
            m = self._success_message()
        except Exception as e:
            print(f"......connection failed. Reason: {e}\a")
            m = self._error_message(e)

        # Note: 'MSH' row string does not show for the message in console in this case
        # text = bytearray(m.to_mllp(), 'utf-8')
        btext = bytearray(''.join([child.to_er7() + '\n' for child in m.children]), 'utf-8')
        if SHOW_RESULT_TO_BROWSER:
            return self.HTML_HEADER + btext + b'<br><br>'
        return btext

    def _error_message(self, exception: Exception) -> Message:
        m = Message(self.NAME)
        m.msh.msh_9 = 'W01'  # W01	ORU - Waveform result, unsolicited transmission of requested information
        m.msh.msh_10 = "000"
        m.msh.msh_11 = "D"  # Current processing, transmitted at intervals (scheduled or on demand) - Debugging
        m.msh.msh_16 = "ER"  # Error/reject conditions only

        # Message Acknowledgment
        msa = Segment("MSA")
        m.add(msa)
        msa.msa_1 = "AE"
        msa.msa_2 = f'Error at {exception}'

        m.validate()
        return m

    def _success_message(self) -> Message:
        text: str = ','.join([f'{abbr}:{random.randint(0, 300)}' for abbr in STRUCTURE_DATA.keys()])

        m = Message(self.NAME)
        m.msh.msh_9 = 'U09'  # ESR/ACK - Automated equipment status request
        m.msh.msh_10 = "888"
        m.msh.msh_11 = "T"  # Current processing, transmitted at intervals (scheduled or on demand)
        m.msh.msh_16 = "AL"  # Always

        # Message Acknowledgment
        msa = Segment("MSA")
        m.add(msa)
        # Acknowledgment Code = Original mode: Application Accept - Enhanced mode: Application acknowledgment: Accept
        m.msa.msa_1 = "AA"
        # MSA.2 - Message Control ID
        m.msa.msa_2 = text

        m.validate()
        return m

