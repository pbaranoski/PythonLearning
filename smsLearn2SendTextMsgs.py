# send text messages
from sms4 import send, nonblocking_send

# result is a json server response. see docs for details
result = send('+4436531593', 'Python calling!')
print(result)