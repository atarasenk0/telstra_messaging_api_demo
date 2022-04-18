#!/usr/bin/python3

# A.Tarasenko
# https://github.com/atarasenk0/telstra_messaging_api_demo.git

# Simple round of tests before submission

from main import *
from dataclasses import dataclass

@dataclass
class test_data_template:
    name:             str
    register_number:  str
    recipient_number: str
    message:          str

test_data = test_data_template("Bob", "0412345678", "0412345678", "Message placeholder")

# ---------------------------------------------------------
# Test number registration
# ---------------------------------------------------------
register_number = test_data.register_number
def test_bnum_registration():
    return register_target_numbers()
# ---------------------------------------------------------


# ---------------------------------------------------------
# Test number provision
# ---------------------------------------------------------
def test_subscription():
    return acquire_subscription()
# ---------------------------------------------------------


# ---------------------------------------------------------
# Test sms send function
# ---------------------------------------------------------
def test_send_sms(sender_name, recipient_number, recipient_message):
    return send_sms(sender_name, recipient_number, recipient_message)
# ---------------------------------------------------------

# ---------------------------------------------------------
# Test sms status check function
# ---------------------------------------------------------
def test_check_sms(sent_sms):
    return get_status_sms(sent_sms)
# ---------------------------------------------------------

# ---------------------------------------------------------
# Check receipt of sms replies
# ---------------------------------------------------------
def test_reply_sms():
    return get_reply_sms()
# ---------------------------------------------------------


if __name__ == "__main__":
    # Create an instance of the API class
    # N.B.: oauth step is handled implicitly under sms.send()
    CONFIG.tls_client_key    = client_key
    CONFIG.tls_client_secret = client_secret

    status_register  = test_bnum_registration()
    status_provision = test_subscription()

    sent_sms        = test_send_sms(test_data.name, test_data.recipient_number, test_data.message)
    sent_sms_status = test_check_sms(sent_sms)

    reply_sms       = test_reply_sms()

    if CONFIG:
        print("CONFIG object: SUCCESS")
    else:
         print("CONFIG object: FAIL")
    
    if (status_register and status_provision):
        print("Number registration: SUCCESS")
    else:
        print("Number registration: FAIL")

    if (sent_sms):
        print("Send sms: SUCCESS")
    else:
        print("Send sms: FAIL")

    if (sent_sms_status):
        print("Check sms status: SUCCESS")
    else:
        print("Check sms status: FAIL")

    if (reply_sms):
        print("Reply sms: SUCCESS")
    else:
        print("Reply sms: FAIL / or no unread messages")

    print("------ End of testing ------")



