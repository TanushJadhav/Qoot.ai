from mahaNLP.tokenizer import Tokenize
from keras.models import model_from_json
import sys
import pandas as pd
import numpy as np
import string
from keras.preprocessing.text import Tokenizer
import keras.utils as ku
from keras.utils import pad_sequences

def english_quotes_generation():
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


def marathi_quotes_generation():
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


from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__, template_folder='../templates')

@app.route('/quotes_gen', methods=['POST', 'GET'])
def quotes():
    
if __name__ == '__main__':
    app.run(port=3000, debug=True)