# Telstra Messaging API Demo
Demo utilising [Telstra Messaging API (2.2.10)](https://dev.telstra.com/content/messaging-api)

### Overview
This prototype-quality client/server application utilises the [Telstra Messaging API (2.2.10)](https://dev.telstra.com/content/messaging-api) and the [Flask web framework](https://flask.palletsprojects.com/en/2.1.x/). This application allows the user to send an SMS message to the registered number.

### Setup
This application was tested in a virtual environment setup with ==Python 3.8.5==

> python3 -m venv env
> source env/bin/activate

Install required packages using ==pip==

> pip install -r requirements.txt

Indicate the location of the Flask application (i.e. main.py):

> export FLASK_APP=main

Execute Flask in the development mode:

> export FLASK_ENV=development

Finally, run the application:

> Flask run

Application should now be running locally on the URL http://127.0.0.1:5000/

### References
- Telstra Dev account: [https://dev.telstra.com/tdev/user/register](https://dev.telstra.com/tdev/user/register)
- Python SDK: [https://github.com/telstra/MessagingAPI-SDK-python/tree/refactor/modernize-sdk](https://github.com/telstra/MessagingAPI-SDK-python/tree/refactor/modernize-sdk)
