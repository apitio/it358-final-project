from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os
from twilio.rest import Client
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
CORS(app)

@app.route('/sendmessage', methods=['GET'])
def send_blast():

    name = request.args.get('name')
    message = request.args.get('message')
    number = request.args.get('number')

    account_sid = os.environ.get("account_sid")
    auth_token = os.environ.get("auth_token")

    print(name)
    print(number)

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=f"Message sent by {name}. {message}",
                        from_='+14153608145',
                        to={number}
                    )


    print(message.sid)
    resp = jsonify(success=True)


    return resp

@app.route('/<scriptName>/<month>/<day>/<cycle>', methods=['GET'])
def respond(scriptName, month, day, cycle):
    response = {}
    script = {}

    print(f"Running Script: {scriptName}")
    print("added cors")

    #error handling for script name
    if not scriptName:
        response["Error"] = "Please enter the script name!"

        return jsonify(response)

    elif str(scriptName).isdigit():
        response["Error"] = "The first parameter cannot be a digit! Please enter valid characters!"

        return jsonify(response)

    else:
        script["name"] = scriptName


    #error handling for month
    if not month:
        response["Error"] = "Please enter the month!"

        return jsonify(response)
    
    elif int(month) < 1 or int(month) > 12:
        response["Error"] = "The month should be between 1-12!"

        return jsonify(response)

    else:
        script["month"] = month


    #error handling for day
    if not day:
        response["Error"] = "Please enter the day!"

        return jsonify(response)
    
    elif int(day) < 1 or int(day) > 31:
        response["Error"] = "The day should be between 1-31!"

        return jsonify(response)

    else:
        script["day"] = day


    #error handling for cycle
    if not cycle:
        response["Error"] = "Please enter valid cycle from 1-10!"

        return jsonify(response)

    elif int(cycle) < 1 or int(cycle) > 10:
        response["Error"] = "The cycle should be between 1-10!"

        return jsonify(response)

    else:
        script["cycle"] = cycle


    #do a dummy run for the script
    script["response"] = "The script has been run succesfully!"

    time.sleep(5)

    return jsonify(script)


@app.route('/')
def index():
    print("Connected to the server!")
    return "<h1>Connected to the server!</h1>"


if __name__ == '__main__':
    #app.run(threaded=True, port=5000)
    #app.run(debug = True, host = '0.0.0.0')

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
