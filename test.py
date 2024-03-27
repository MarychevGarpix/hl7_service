from server.oru_r01_message_mixin import ORUR01MessageMixin

oru = ORUR01MessageMixin()

message = oru.prepare_message()
assert message is not type(bytes), 'Неверный тип сообщения'
print(message)

