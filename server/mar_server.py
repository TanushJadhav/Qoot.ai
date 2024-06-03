import numpy as np
import pandas as pd
from mahaNLP.tokenizer import Tokenize
from keras.models import model_from_json
import sys

file = open('MAR_model\model.json', 'r')
loaded  = file.read()
file.close()

model = model_from_json(loaded)
model.load_weights("MAR_model\model.h5")


df = pd.read_csv('MAR_model\Marathi_quotes.txt', sep="\t", header = None)

text = []
for i in df[0]:
  text.append(i)

maxlen = 18
step = 6
sentences = []
next_chars = []

for quote in text:
    for i in range(0, len(quote) - maxlen, step):
        sentences.append(quote[i: i + maxlen])
        next_chars.append(quote[i + maxlen])
    sentences.append(quote[-maxlen:])
    next_chars.append(quote[-1])

t = ' '.join(text)
chars = sorted(list(set(t)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

tokenizer = Tokenize()

two_first_words = [bigram for bigram in [' '.join(tokenizer.word_tokenize(quote)[:4]) for quote in text] if len(bigram) <= maxlen]

def sample(preds, temperature=0.3):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generate_quote(sentence = None, diversity = 0.5):
    
    if not sentence: ## if input is null then sample two first word from dataset
        random_index = np.random.randint(0, len(two_first_words))
        sentence = two_first_words[random_index]
        
    if len(sentence) > maxlen:
        sentence = sentence[-maxlen:]
    elif len(sentence) < maxlen:
        sentence = ' '*(maxlen - len(sentence)) + sentence
        
    generated = ''
    generated += sentence
    sys.stdout.write(generated)
    
    next_char = 'Empty'
    total_word = 0 
    
    max_word = 6
    
    while ((next_char not in ['\n', '.']) & (total_word <= max_word)):
    
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]

        if next_char == ' ':
           total_word += 1
        generated += next_char
        sentence = sentence[1:] + next_char

    return generated


    
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/mar_quotes', methods=['POST', 'GET'])
def mar_quotes():
    generated_quote = generate_quote()
    return jsonify({'quote': generated_quote})

if __name__ == '__main__':
    app.run(port=4000, debug=True)
    