from collections import defaultdict

# Define a weighted dictionary of words associated with each intent
intent_weights = {
    "configure": {"config": 2, "set": 1, "enable": 1, "router": 1},
    "show": {"get": 1, "show": 2, "display": 1, "status": 1},
    "run command": {"run": 2, "command": 1, "execute": 1},
    "check status": {"check": 2, "status": 1, "verify": 1},
}

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

# Test the function with different sentences
test_sentences = [
    "Please config the router with new settings.",
    "Could you show the status of the device?",
    "Run command A on router B",
    "Check the status of router C",
    "give me the output of the command B on router A",
    "execute the command A on router B",
    "show the output of command B on router A"
]

for sentence in test_sentences:
    intent, score = calculate_intent_score(sentence, intent_weights)
    print(f"Sentence: '{sentence}'")
    print(f"Predicted Intent: '{intent}' with score {score}\n")

