import logging
import json
import requests
import os
import boto.sqs
from boto.sqs.message import RawMessage


import flask
from flask import request, Response, Flask, jsonify, abort, make_response


# Create and configure the Flask app
application = flask.Flask(__name__)
application.config.from_object('default_config')
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']

@application.route('/send-email', methods=['POST'])
def send_email():
    """Send an e-mail using Mailgun"""

    response = None
    if request.json is None:
        # Expect application/json request
        response = Response("", status=415)
    else:
        message = dict()
        try:
            message = request.json

            send_simple_message( message['to'], message['from'],
                                message['subject'], message['body'])
            response = Response("", status=200)
        except Exception as ex:
            logging.exception('Error processing message: %s' % request.json)
            response = Response(ex.message, status=500)

    return response

def send_simple_message(to, from_email, body, subject):
    return requests.post(
        os.environ['MAILGUN_DOMAIN'],
        auth=("api", os.environ['MAILGUN_API_KEY']),
        data={"from": from_email,
              "to": [to],
              "subject": subject,
              "text": body
        })


if __name__ == '__main__':
    application.run(host='0.0.0.0')