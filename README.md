# Telstra Messaging API Demo
Demo utilising [Telstra Messaging API (2.2.10)](https://dev.telstra.com/content/messaging-api)

### Overview
This prototype-quality client/server application utilises the [Telstra Messaging API (2.2.10)](https://dev.telstra.com/content/messaging-api) and the [Flask web framework](https://flask.palletsprojects.com/en/2.1.x/). This application allows the user to send an SMS message to the registered number.

### Setup
This application was tested in a virtual environment setup with ```Python 3.8.5```

> python3 -m venv env
> 
> source env/bin/activate

Install required packages using ```pip```

> pip install -r requirements.txt

Update the values of the following variables in main.py file:
```
register_numbers = ["0412345678"]
client_key       = "<client_key>"
client_secret    = "<client_secret>"
```

Indicate the location of the ```Flask``` application (i.e. main.py):

> export FLASK_APP=main

Execute ```Flask``` in the development mode:

> export FLASK_ENV=development

Finally, run the application:

> Flask run

Application should now be running locally on the URL: http://127.0.0.1:5000/

### Wish list
- Containerisation / public hosting of the application
- Perform proper session authentication
- Maintain user input even after a submit event (i.e. avoid page refreshes)
- Improve client design/appearance

### References
- [Telstra Dev Portal](https://dev.telstra.com/tdev/user/register)
- [Messaging API Python SDK](https://github.com/telstra/MessagingAPI-SDK-python/tree/refactor/modernize-sdk)
- [How To Make a Web Application Using Flask in Python 3](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3)
- [How to build a web application using Flask and deploy it to the cloud](https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/)
