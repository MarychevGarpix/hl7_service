import random
from enum import Enum

from hl7apy.core import Message, Segment, Group
from hl7apy.parser import parse_message

from mock_data import STRUCTURE_DATA
from server.conf import SHOW_RESULT_TO_BROWSER, SERVICE_NAME


class MSH11ProcessingId(str, Enum):
    PRODUCTION = 'P'
    DEBUGGING = 'D'


class MSH16ApplicationAcknowledgmentType(str, Enum):
    ALWAYS = 'AL'
    ERROR = 'ER'


class ORUR01Choice:
    MSH11ProcessingId = MSH11ProcessingId
    MSH16ApplicationAcknowledgmentType = MSH16ApplicationAcknowledgmentType


class ORUR01MessageMixin:
    """
    Info about ORU^R01 messages:
    * https://hl7-definition.caristix.com/v2/HL7v2.6/TriggerEvents/ORU_R01
    * https://www.interfaceware.com/hl7-oru
    """
    NAME: str = 'ORU_R01'
    MESSAGE_TYPE: str = 'ORU^R01^ORU_R01'  # Unsolicited transmission of an observation message
    MESSAGE_CONTROL_ID: str = '1433'
    OBSERVATION_GROUP: str = 'ORU_R01_OBSERVATION'
    HTML_HEADER: bytes = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.encode('utf-8')

    def prepare_message(self) -> bytes:
        try:
            m = self._success_message()
        except Exception as e:
            print(f"......connection failed. Reason: {e}\a")
            m = self._error_message(e)

        btext = bytearray(m.to_er7(trailing_children=True).replace('\r', '\n'), 'utf-8')
        if SHOW_RESULT_TO_BROWSER:
            return self.HTML_HEADER + btext + b'<br><br>'
        return btext + b'\r\n'

    def _error_message(self, exception: Exception) -> Message:
        m = Message(self.NAME)

        # Message Header
        m.msh.msh_3 = SERVICE_NAME
        m.msh.msh_9 = self.MESSAGE_TYPE
        m.msh.msh_10 = self.MESSAGE_CONTROL_ID
        m.msh.msh_11 = ORUR01Choice.MSH11ProcessingId.PRODUCTION
        m.msh.msh_16 = ORUR01Choice.MSH16ApplicationAcknowledgmentType.ERROR

        # PID - Patient Identification
        m.ORU_R01_PATIENT_RESULT.ORU_R01_PATIENT.PID.pid_3 = "1"
        m.ORU_R01_PATIENT_RESULT.ORU_R01_PATIENT.PID.pid_5 = "Hospital"
        # OBR Segment -- Patient details -- Observation Request
        m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.OBR.obr_4 = "L"

        # obx groups
        index = 1
        obx_group = Group(self.OBSERVATION_GROUP)
        obx = Segment('OBX')
        obx.obx_1 = str(index)
        obx.obx_2 = "NM"
        obx.obx_3 = str(exception)
        obx.obx_4 = 'Error'
        obx.obx_11 = "F"
        obx_group.add(obx)
        m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.add(obx_group)

        m.validate()
        return m

    def _success_message(self) -> Message:
        m = Message(self.NAME)

        # Message Header
        m.msh.msh_3 = SERVICE_NAME
        m.msh.msh_9 = self.MESSAGE_TYPE
        m.msh.msh_10 = self.MESSAGE_CONTROL_ID
        m.msh.msh_11 = ORUR01Choice.MSH11ProcessingId.PRODUCTION
        m.msh.msh_16 = ORUR01Choice.MSH16ApplicationAcknowledgmentType.ALWAYS

        # PID - Patient Identification
        m.ORU_R01_PATIENT_RESULT.ORU_R01_PATIENT.PID.pid_3 = "1"
        m.ORU_R01_PATIENT_RESULT.ORU_R01_PATIENT.PID.pid_5 = "Hospital"
        # OBR Segment -- Patient details -- Observation Request
        m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.OBR.obr_4 = "L"

        # obx groups
        index = 1
        for tag_name, abbr in STRUCTURE_DATA.items():
            obx_group = Group(self.OBSERVATION_GROUP)
            obx = Segment('OBX')
            obx.obx_1 = str(index)
            obx.obx_2 = "NM"
            obx.obx_3 = tag_name
            obx.obx_4 = abbr
            obx.obx_5 = str(random.randint(0, 300))
            obx.obx_11 = "F"
            obx_group.add(obx)
            m.ORU_R01_PATIENT_RESULT.ORU_R01_ORDER_OBSERVATION.add(obx_group)
            index += 1

        m.validate()
        return m

    @staticmethod
    def _message_valid() -> Message:
        obx_list = []
        index = 1
        for tag_name, abbr in STRUCTURE_DATA.items():
            obx = Segment('OBX')
            obx.obx_11 = 'R'  # Observation Result Status:
            obx.obx_13 = 'Garpix'
            obx.obx_3.obx_3_1 = str(index)
            obx.obx_3.obx_3_2 = tag_name
            obx.obx_3.obx_3_3 = str(random.randint(0, 300))
            obx.obx_3.obx_3_4 = abbr
            obx_list.append(obx)

            index += 1

        text: str = '\r'.join([obx.to_er7() for obx in obx_list])
        msh = 'MSH|^~\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|20120309132638||ORU^R01|Q162690178T166106789|P|2.5\r'
        pid = 'PID|1||000168674|000168674|GUNN^BEBE||19821201|F||||||||M|||890-12-3456|||N||||||||N\r'
        pv1 = 'PV1||O|60|1|||01931^PHYSICIAN^THOMAS^W.^^DR|||60||||1||N|01487^PHYSICIAN^JONATHAN^F|3|10478417|21|||||||||||||||||||01|||||201209201932|||||||V\r'
        obr = 'OBR||00013598436|R-GEN-378456-2-1|CST2^CHEST 2 VIEWS|||201209202036|||||||||01931^PHYSICIAN^THOMAS^W.^^DR||888024||||20120920230242||XY|||1^^^201209202036^201209202036^S|WEB^PHYSICIAN^JONATHAN^F^^^^^^^^^ADMIT^WEB&WEBCHART OFFICES|||^fever|39023^PHYSICIAN^PAUL^R^^DR|39023^PHYSICIAN^PAUL^R^^DR\r'
        obx1 = 'OBX|1|HD|SR Instance UID||1.113654.1.2001.30.2.1||||||F||||||\r'
        obx2 = 'OBX|2|TX|SR Text||Radiology Report History Cough Findings PA evaluation of the chest demonstrates the lungs to be expanded and clear.  Conclusions Normal PA chest x-ray.||||||F||||||\r'
        cti = 'CTI|study1|^1|^10_EP1\r'

        return parse_message(msh + pid + pv1 + obr + text + obx1 + obx2 + cti)

    @staticmethod
    def _message_not_valid() -> Message:
        # Note: Only to check from IVL-738 issue
        msh = 'MSH|^~\&|Sending App||||20230627123536000+0000||ORU^R01|1433|P|2.6|||AL|NE||UNICODE UTF-8|||\r'
        pid = 'PID|||^^Hospital^PI||^^^^^L|||M||unknownrace\r'
        obx1 = 'OBX|1|NM|TIDAL_VOLUME_EXP||100|MILL|||||R|||20230627123536+0000\r'
        obx2 = 'OBX|2|NM|TIDAL_VOLUME_INSP||100|MILL|||||R|||20230627123536+0000\r'
        obx3 = 'OBX|3|NM|MINUTE_VOLUME_EXP||100|L|||||R|||20230627123536+0000\r'
        m = parse_message(msh + pid + obx1 + obx2 + obx3)

        for c in m.children:
            print(c)

        m.validate()
        return m
