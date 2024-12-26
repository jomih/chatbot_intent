from flask import Flask, request, render_template
import json, os, re
#CORS to mitigate CORS errors - a type of error related to making requests to domains other than the one that hosts this webpage
from flask_cors import CORS
from collections import defaultdict

import collect_info


#from transformers import AutoModelForSeq2SeqLM
#from transformers import AutoTokenizer

#hugging face certificate
#os.environ['CURL_CA_BUNDLE'] = './huggingface.co.pem'


# Define a weighted dictionary of words associated with each intent
intent_weights = {
    "configure": {"config": 2, "set": 1, "enable": 1, "router": 1},
    "show": {"get": 1, "show": 2, "display": 1, "status": 1},
    "run command": {"run": 2, "command": 1, "execute": 1, "show" : 1, "output":1},
    "check status": {"check": 2, "status": 1, "verify": 1, "tests": 1, "checks": 1},
}

# Function to extract the command and the router

def extract_command_and_router(sentence):
    # Define a regex pattern to capture the command and router
    pattern = r"(?:run|execute)(?: the command| command)?\s+([\w\s]+?)\s+(?:in|on|at) (?:router\s+)?(\w+)"
    # (?: ... ) is a non-capturing group
    # (...)?  makes it optional

    match = re.search(pattern, sentence.lower())
    
    if match:
        command = match.group(1).strip()
        router = match.group(2).strip()
        return command, router
    else:
        return None, None

def calculate_intent_score(sentence, intent_weights):
    # Tokenize the sentence (simple split by spaces here, you might use a more sophisticated tokenizer if needed)
    words = sentence.lower().split()
    
    # Calculate scores for each intent based on the presence and weight of words
    scores = defaultdict(int)
    for intent, keywords in intent_weights.items():
        for word in words:
            if word in keywords:
                scores[intent] += keywords[word]
    
    # Determine the intent with the highest score
    if scores:
        best_intent = max(scores, key=scores.get)
        return best_intent, scores[best_intent]
    else:
        return None, 0

#Model initialization
#model_name = "facebook/blenderbot-400M-distill"
#model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
#tokenizer = AutoTokenizer.from_pretrained(model_name)

#conversation_history = []

app = Flask("MyChatBot")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/chatbot', methods=['POST'])
def handle_prompt():
    # Read prompt from HTTP request body
    data = request.get_data(as_text=True)
    data = json.loads(data)
    message = data['prompt']
    print('got message: ', message)
    #input_text = data['prompt']
    
    response = calculate_intent_score(sentence=message, intent_weights=intent_weights)
    command, router = extract_command_and_router(sentence=message)
    print('intention identified: ', response)
    print('router is: ', router)
    print('command is: ', command)
    
    #llamada a script de conexion
    response = collect_info.collect_info(router, command)

    #return response
    return response


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)