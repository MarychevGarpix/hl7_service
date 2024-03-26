import random
from enum import Enum

from hl7apy.core import Message, Segment, Group, Field
from hl7apy.parser import parse_message

from mock_data import STRUCTURE_DATA
from server.conf import SHOW_RESULT_TO_BROWSER


class MSH11ProcessingId(str, Enum):
    PRODUCTION = 'P'
    DEBUGGING = 'D'


class MSH16ApplicationAcknowledgmentType(str, Enum):
    ALWAYS = 'AL'
    ERROR = 'ER'


class ORUR01Choice:
    mSH11ProcessingId = MSH11ProcessingId
    MSH16ApplicationAcknowledgmentType = MSH16ApplicationAcknowledgmentType


class ORUR01MessageMixin:
    """
    Info about ORU^R01 messages:
    * https://hl7-definition.caristix.com/v2/HL7v2.6/TriggerEvents/ORU_R01
    * https://www.interfaceware.com/hl7-oru
    """
    NAME: str = 'ORU_R01'
    MESSAGE_TYPE: str = 'R01'  # Unsolicited transmission of an observation message
    MESSAGE_CONTROL_ID: str = '1433'
    # PATIENT_RESULT_GROUP: str = 'ORU_R01_PATIENT_RESULT'
    # ORDER_OBSERVATION: str = 'ORU_R01_ORDER_OBSERVATION'
    # PATIENT_GROUP: str = 'ORU_R01_PATIENT'

    # The Observation Request (OBR) segment is used to transmit information specific to an order for a diagnostic study or observation, physical exam, or assessment.

    HTML_HEADER: bytes = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.encode('utf-8')

    def prepare_ack_message(self) -> bytes:
        # try:
        m = self._success_message()
        # except Exception as e:
        #     print(f"......connection failed. Reason: {e}\a")
        #     m = self._error_message(e)

        # Note: 'MSH' row string does not show for the message in console in this case
        # text = bytearray(m.to_mllp(), 'utf-8')
        btext = bytearray(''.join([child.to_er7() + '\n' for child in m.children]), 'utf-8')
        # if SHOW_RESULT_TO_BROWSER:
        #     return self.HTML_HEADER + btext + b'<br><br>'
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
        # text: str = ','.join([f'{abbr}:{random.randint(0, 300)}' for abbr in STRUCTURE_DATA.keys()])

        # m = Message(self.NAME)
        # m.msh.msh_9 = self.MESSAGE_TYPE
        # m.msh.msh_10 = self.MESSAGE_CONTROL_ID
        # m.msh.msh_11 = ORUR01Choice.mSH11ProcessingId.PRODUCTION
        # m.msh.msh_16 = ORUR01Choice.MSH16ApplicationAcknowledgmentType.ALWAYS
        #
        # patient_result = Group('ORU_R01_PATIENT_RESULT')
        # _patient = Group('ORU_R01_PATIENT')
        # patient_result.add(_patient)
        #
        # _patient.add_segment('PID')
        # _patient.pid.pid_3 = 'Hospital'
        # _patient.pid.pid_5 = 'PI'  # Patient internal identifier
        #
        # _order_observation = Group('ORU_R01_ORDER_OBSERVATION')
        # patient_result.add(_order_observation)
        # m.add(patient_result)
        #
        # _order_observation.add_segment('OBX')
        # _order_observation.obx.obx_3.obx_3_1 = '1'
        # _order_observation.obx.obx_3.obx_3_2 = 'TIDAL_VOLUME'
        # _order_observation.obx.obx_3.obx_3_3 = '333'
        # _order_observation.obx.obx_3.obx_3_4 = 'Vt'
        m = self._success_message_valid()

        # for c in m.children:
        #     print('>> ', c.to_er7())
            # for f in c.children:
            #     print('. ', f.to_er7())
            #     for i in f.children:
            #         print('. . ', i)

        btext = bytearray(''.join([child.to_er7() + '\n' for child in m.children]), 'utf-8')
        print(btext)

        m.validate()

        return m

    @staticmethod
    def _success_message_valid() -> Message:
        # text: str = ','.join([f'{abbr}:{random.randint(0, 300)}' for abbr in STRUCTURE_DATA.keys()])
        # obx_list = [
        #     f'OBX|NM|{index}|{tag}|{random.randint(0, 300)}|||1.113654.1.2001.30.2.1||||||F||||||\r'
        #     for index, tag in enumerate(STRUCTURE_DATA.keys())
        # ]

        obx_list = []
        for index, abbr in enumerate(STRUCTURE_DATA.keys()):
            obx = Segment('OBX')
            obx.obx_11 = 'R'
            obx.obx_13 = 'Garpix'
            obx.obx_3.obx_3_1 = str(index)
            obx.obx_3.obx_3_2 = 'ABBR'
            obx.obx_3.obx_3_3 = str(random.randint(0, 300))
            obx.obx_3.obx_3_4 = abbr
            obx_list.append(obx)


        text: str = '\r'.join([obx.to_er7() for obx in obx_list])
        print(text)

        msh = 'MSH|^~\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|20120309132638||ORU^R01|Q162690178T166106789|P|2.5\r'
        pid = 'PID|1||000168674|000168674|GUNN^BEBE||19821201|F||||||||M|||890-12-3456|||N||||||||N\r'
        pv1 = 'PV1||O|60|1|||01931^PHYSICIAN^THOMAS^W.^^DR|||60||||1||N|01487^PHYSICIAN^JONATHAN^F|3|10478417|21|||||||||||||||||||01|||||201209201932|||||||V\r'
        obr = 'OBR||00013598436|R-GEN-378456-2-1|CST2^CHEST 2 VIEWS|||201209202036|||||||||01931^PHYSICIAN^THOMAS^W.^^DR||888024||||20120920230242||XY|||1^^^201209202036^201209202036^S|WEB^PHYSICIAN^JONATHAN^F^^^^^^^^^ADMIT^WEB&WEBCHART OFFICES|||^fever|39023^PHYSICIAN^PAUL^R^^DR|39023^PHYSICIAN^PAUL^R^^DR\r'
        obx1 = 'OBX|1|HD|SR Instance UID||1.113654.1.2001.30.2.1||||||F||||||\r'
        obx2 = 'OBX|2|TX|SR Text||Radiology Report History Cough Findings PA evaluation of the chest demonstrates the lungs to be expanded and clear.  Conclusions Normal PA chest x-ray.||||||F||||||\r'
        cti = 'CTI|study1|^1|^10_EP1\r'
        return parse_message(msh + pid + pv1 + obr + text + cti)

    @staticmethod
    def oru_r01_not_valid_message_example():
        # Note: Only to check from IVL-738 issue
        msh = 'MSH|^~\&|Sending App||||20230627123536000+0000||ORU^R01|1433|P|2.6|||AL|NE||UNICODE UTF-8|||\r'
        pid = 'PID|||^^Hospital^PI||^^^^^L|||M||unknownrace\r'
        obx1 = 'OBX|1|NM|TIDAL_VOLUME_EXP||100|MILL|||||R|||20230627123536+0000\r'
        obx2 = 'OBX|2|NM|TIDAL_VOLUME_INSP||100|MILL|||||R|||20230627123536+0000\r'
        obx3 = 'OBX|3|NM|MINUTE_VOLUME_EXP||100|L|||||R|||20230627123536+0000\r'
        m = parse_message(msh + pid + obx1 + obx2 + obx3)
        for c in m.children:
            print(c)
            for f in c.children:
                print('. ', f)
                for i in f.children:
                    print('. . ', i)

        m.validate()
        return m
