from typing import Dict
from flask import Flask, request
import requests
import json
app=Flask(__name__)

@app.route("/wave", methods=["GET"])
def wave():
    return "Hola Mundo from Flask babe"

@app.route("/whatsapp", methods=["GET"])
def verify_token():
    try:
        access_token="mysecretaccesstoken"
        token=request.args.get("hub.verify_token")
        challenge=request.args.get("hub.challenge")

        if token == access_token:
            return challenge
        else:
            return "error", 400
    except:
        return "error", 400

@app.route("/whatsapp", methods=["POST"])
def received_message():
    try:
        body=request.get_json()
        entry=body["entry"][0]
        changes=entry["changes"][0]
        value=changes["value"]
        message=value["messages"][0]
        text=message["text"]
        question_user=text["body"]
        number=message["from"]

        print("Este es el texto del usuario: ", question_user)

        body_answer=send_message(question_user,number )
        send_message_var=whatsapp_service(body_answer)

        if send_message_var:
            print("Mensaje Enviado Correctamente")
        else:
            print("error al envio de mensaje")

        return "EVENT_RECEIVED"
    except Exception as e:
        print(e)
        return "EVENT_RECEIVED"

def whatsapp_service(body):

    try:
        token="EAAOXe8l51JcBO5RUbFDe04cbsfZAY1bZB6Ct1vXQ2MCL4LpZCHboluLmb1D4nRytgBZAQNKAmkBuVBrxGjhB8Umbu4gzbsnZB07a2WZCIeVvCgIGvo3h9KM7YzhpqmPHPsPOtY0aTZCJ1m7oxol0Ai0wyZCUFltcLZATnAA1oYkktfQZA1zwKQyaeIG1OR3JB8wqTM"
        api_url="https://graph.facebook.com/v19.0/354291281096365/messages"
        headers: Dict[str, str] = {
            'Content-Type':'application/json',
            'Authorization': f'Bearer {token}'
        }

        response=requests.post(api_url, data=json.dumps(body), headers=headers)

        if response.status_code==200:
            return True
        else:
            return False
        
    except Exception as e:
        print(e)

        return False


def send_message(text, number):
    body = {
        "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
    }

    return body


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8502, debug=True)
