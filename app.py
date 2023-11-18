from flask import Flask, request, jsonify
import asyncio

from irish_name_pronouncer.api import get_response, parse_example
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_status():
    return 'healthy'

@app.route('/name_pronunciation', methods=['POST'])
def get_pronunciation():
    name = request.json['name']
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print("Getting response...")
    assistant_message = loop.run_until_complete(get_response(name))
    print("Response: ", assistant_message)
    name, pronc = parse_example(assistant_message.content)
    print(name, pronc)

    return jsonify({'pronunciation': pronc})
    
if __name__ == '__main__':
    app.run()