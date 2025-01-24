from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_message = request.form.get('Body')

    if incoming_message:
        print(f"Message: {incoming_message}")
    else:
        print("No message body found.")

    response = MessagingResponse()
    response.message(f"Received your message: {incoming_message}")

    return str(response)

@app.route("/", methods=['GET'])
def home():
    return "Flask server is running!"


if __name__ == "__main__":
    app.run(debug=True)
