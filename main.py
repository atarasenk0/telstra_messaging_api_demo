#!/usr/bin/python3

from flask import Flask, render_template, request, flash, redirect, url_for
from tls.messaging.utils.config import CONFIG
from tls.messaging.utils import phone_number
from tls.messaging import bnum
from tls.messaging import sms
from tls.messaging import subscription
from tls.messaging import exceptions

# ---------------------------------------------------------
# Modify these attributes/variables/constants only
# ---------------------------------------------------------
DEBUG            = True
register_numbers = ["0435123456"]
client_key       = "DXyWZKp4dQxFBOhQYLtAH3pnyAT8f9j"
client_secret    = "fiHDlraTXML8kb0"
flask_secret_key = "abc"
# ---------------------------------------------------------

# ---------------------------------------------------------
# Step 1. Perform client authentication
# Should be done before any interaction e.g. sending SMS
# https://dev.telstra.com/content/messaging-api#operation/authToken
# https://github.com/telstra/MessagingAPI-SDK-python/tree/refactor/modernize-sdk#authentication
# ---------------------------------------------------------

# Create an instance of the API class
# N.B.: oauth step is handled implicitly under sms.send()
CONFIG.tls_client_key    = client_key
CONFIG.tls_client_secret = client_secret
if DEBUG:
    print("Config object: %s\n" % CONFIG)
# ---------------------------------------------------------


# ---------------------------------------------------------
# Step 2. Register the target numbers / create subscription
# https://dev.telstra.com/content/messaging-api#operation/freeTrialBnumRegister
# https://github.com/telstra/MessagingAPI-SDK-python/tree/refactor/modernize-sdk#registering-destinations
# ---------------------------------------------------------
# TODO: check if the registered numbers field is empty?
try:
    phone_numbers = bnum.register(phone_numbers=register_numbers)
    if DEBUG:
        print("Number(s) to register: %s\n" % phone_numbers)
    
    retrieved_numbers = bnum.get()
    if DEBUG:
        print("Registered number(s): %s\n" % retrieved_numbers)

except exceptions.BnumError as e:
    print("Exception when calling bnum.register: %s\n" % e)
# ---------------------------------------------------------


# ---------------------------------------------------------
# Step 3. Acquire the current subscription number 
# https://dev.telstra.com/content/messaging-api#operation/createSubscription
# https://github.com/telstra/MessagingAPI-SDK-python/tree/refactor/modernize-sdk#subscription
# ---------------------------------------------------------
# TODO: check if the assigned number already exists?
try: 
    created_subscription = subscription.create()
    if DEBUG:
        print("Subscription object: %s\n" % created_subscription)
    
    retrieved_subscription = subscription.get()
    if DEBUG:
        print("Subscribed object: %s\n" % retrieved_subscription)

except exceptions.SubscriptionError as e: 
    print("Exception when calling subscription.create: %s\n" % e)
# ---------------------------------------------------------


# ---------------------------------------------------------
# Function for acquiring/processing the sms status
# https://dev.telstra.com/content/messaging-api#operation/getSmsStatus
# https://github.com/telstra/MessagingAPI-SDK-python/tree/refactor/modernize-sdk#get-sms-status
# ---------------------------------------------------------
def get_status_sms(sent_sms):
    try:
        status = sms.get_status(sent_sms.message_id)
        if DEBUG:
            print("Sent sms status: %s\n" % status)
        
        return status
    except exceptions.SmsError as e: 
        print("Exception when calling sms.send: %s\n" % e)
        return -1
# ---------------------------------------------------------


# ---------------------------------------------------------
# Function for acquiring the inbound SMS 
# https://dev.telstra.com/content/messaging-api#operation/retrieveInboundSms
# https://github.com/telstra/MessagingAPI-SDK-python/tree/refactor/modernize-sdk#retrieve-reply
# ---------------------------------------------------------
def get_reply_sms():
    try: 
        reply_sms = sms.get_next_unread_reply()
        
        if DEBUG:
            print("Received sms: %s\n" % reply_sms)

        return reply_sms
    except exceptions.SmsError as e:
        print("Exception when calling sms.get_next_unread_reply: %s\n" % e)
        return -1
# ---------------------------------------------------------


# ---------------------------------------------------------
# Function for sending the sms message
# https://dev.telstra.com/content/messaging-api#operation/sendSms
# https://github.com/telstra/MessagingAPI-SDK-python/tree/refactor/modernize-sdk#send-sms
# ---------------------------------------------------------
def send_sms(sender_name, recipient_number, recipient_message):
    try: 
        # Please note:
        # - Alphanumeric Sender ID is only available on Telstra Account paid plans, not through Free Trial or Credit Card plans.
        # - Support for Alphanumeric Sender ID is only guaranteed when sending messages to Telstra destinations.
        # Since we are utilising the Free Trial version of the API, sender_name string will not be utilised
        sent_sms = sms.send(to=str(recipient_number), body=str(recipient_message))
        if DEBUG:
            print("Sent sms: %s\n" % sent_sms)
        
        return sent_sms
    except exceptions.SmsError as e: 
        print("Exception when calling sms.send: %s\n" % e)
        return -1
# ---------------------------------------------------------


# ---------------------------------------------------------
# Using flask web framework to interact with client page
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
# https://www.javatpoint.com/flask-flashing
# ---------------------------------------------------------
app = Flask(__name__)
app.secret_key = flask_secret_key 

# ---------------------------------------------------------
# index.html
# ---------------------------------------------------------
@app.route('/index', methods=['GET', 'POST'])
def index():
    if DEBUG:
        print("Triggered method: %s\n" % request.method)
    
    if request.method == 'POST':
        if request.form.get("submit_button") == "Send":
            sender_name       = request.form.get('senderName')
            recipient_number  = request.form.get('recipientNumber')
            recipient_message = request.form.get('recipientMessage')
            
            # Check for the correct user input
            name_valid    = len(str(sender_name)) > 0
            number_valid  = phone_number.check(recipient_number)
            message_valid = len(str(recipient_message)) > 0

            # Only send sms if input is valid
            # No additional processing of status_sms.delivery_status beyond default 
            # Display status of the sent SMS under the button group
            # https://dev.telstra.com/content/messaging-api#operation/getSmsStatus 
            if (name_valid and number_valid.valid and message_valid):
                sent_sms   = send_sms(sender_name, recipient_number, recipient_message)
                status_sms = get_status_sms(sent_sms)
                flash(str(status_sms.delivery_status))
                return render_template('index.html', information=status_sms.delivery_status)
            else:
                return render_template('index.html', error="Please check above inputs...")
        elif request.form.get("check_button") == "Check Response":
            reply_sms = get_reply_sms()

            if reply_sms:
                return render_template('index.html', response=reply_sms.message)
            else:
                return render_template('index.html', response="No unread messages")
        else:
            pass
    else:
        pass 
    return render_template('index.html')
# ---------------------------------------------------------


# ---------------------------------------------------------
# login.html
# No strict user authentications has been implementation
# Login page is for demo purposes only
# Based heavily on the following reference: 
# https://www.javatpoint.com/flask-flashing
# ---------------------------------------------------------
@app.route('/', methods = ["GET","POST"])  
def login():  
    error = None;  
    if request.method == "POST":  
        if request.form.get("submit_button") == "Submit":
            if request.form['pass'] != 'password':  
                error = "invalid password..."  
            else:  
                return redirect(url_for('index'))   
    return render_template('login.html', error=error)
# ---------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)