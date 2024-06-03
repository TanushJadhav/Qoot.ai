import pandas as pd
import numpy as np
import string

from keras.models import model_from_json
from keras.preprocessing.text import Tokenizer
import keras.utils as ku
from keras.utils import pad_sequences

# Loading the model
file = open('ENG_Model\eng_quote_model.json', 'r')
loaded = file.read()
file.close()

model = model_from_json(loaded)
model.load_weights("ENG_Model\eng_quote_model.h5")

# Calling the dataset
df = pd.read_csv('ENG_Model\eng_quotes.csv')
df = df[df["quote"].str.contains('\d') == False]
quotes_list = []

for i in df['quote']:
    quotes_list.append(i)

# Cleaning the texts
def remove_punctuation(text):
    punct = string.punctuation
    punct = punct.replace("'", "")
    text = text.translate(str.maketrans("", "", punct))
    return text

def text_lower(text):
    text = text.lower()
    return text

cleaned_quotes = []
for i in quotes_list:
    text = remove_punctuation(i)
    text = text_lower(str(text))
    cleaned_quotes.append(text)

# Tokenization
tokenizer = Tokenizer()

# Function to create the sequences
def generate_sequences(corpus):
    tokenizer.fit_on_texts(corpus)
    total_words = len(tokenizer.word_index) + 1
    input_sequences = []
    for line in corpus:
        seq = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(seq)):
            ngram_seq = seq[:i + 1]
            input_sequences.append(ngram_seq)
    return input_sequences, total_words

# Generating sequences
input_sequences, total_words = generate_sequences(cleaned_quotes)

# Generating predictors and labels from the padded sequences
def generate_input_sequence(input_sequences):
    maxlen = max([len(x) for x in input_sequences])
    input_sequences = pad_sequences(input_sequences, maxlen=maxlen)
    predictors, label = input_sequences[:, :-1], input_sequences[:, -1]
    label = ku.to_categorical(label, num_classes=total_words)
    return predictors, label, maxlen

predictors, label, maxlen = generate_input_sequence(input_sequences)

# Text generating function
def generate_quote(seed_text, num_words, model, maxlen):
    for _ in range(num_words):
        tokens = tokenizer.texts_to_sequences([seed_text])[0]
        tokens = pad_sequences([tokens], maxlen=maxlen, padding='pre')
        predicted = np.argmax(model.predict(tokens))
        output_word = ''
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text = seed_text + " " + output_word
    return seed_text

import pyttsx3

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/eng_quotes', methods=['POST', 'GET'])
def eng_quotes():
    if request.method == 'POST':
        data = request.json
        seed_text = data.get('seed_text', 'default_seed_text')
        num_words = int(data.get('num_words', 10))  # Default value for num_words is 10

        generated_quote = generate_quote(seed_text, num_words, model, maxlen - 1)

        engine = pyttsx3.init()
        engine.say(generate_quote)
        engine.runAndWait()
        
        return jsonify({'quote': generated_quote})
        
    else:
        return jsonify({'error': 'POST request required'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
