# Python markov chain text generator

import random
import pickle
import os
import string

class Pykvtxt(object):

    def __init__(self, open_file, cache_name):
        self.cache = {}
        self.cache_file = cache_name + ".pkl"
        self.open_file = open_file
        self.words = self.parse_file()
        self.text_size = len(self.words)
        self.database()

    def parse_file(self):
        # load in saved data from file
        # get path of .pkl files
        script_dir = os.path.dirname(__file__)
        rel_path = "pkl/" + self.cache_file
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path,'rb') as f:
            # These 2 lines are only needed once to initially add to files
            #s = f.read()
            #if s:
            self.cache = pickle.load(f)

        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return words

    def genText(self):
        if len(self.words) < 4:
            return

        for i in range(len(self.words) - 3):
            yield(self.words[i], self.words[i + 1], self.words[i + 2],
                  self.words[i + 3])

    def database(self):
        for w1, w2, w3, w4 in self.genText():
            key = (w1, w2, w3)
            if key in self.cache:
                self.cache[key].append(w4)
            else:
                self.cache[key] = [w4]

        # save to file
        script_dir = os.path.dirname(__file__)
        rel_path = "pkl/" + self.cache_file
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path,'wb') as f:
            pickle.dump(self.cache, f, pickle.HIGHEST_PROTOCOL)
            



    def printText(self, size=200):
        # var to check if we're in between a quotation ""
        inQuote = False

        # Number of sentences to generate, and count for later loop

        
        seed = random.randint(0, self.text_size - 4)
        # Start sentence with a capital word so it looks like a real sentence
        while(self.words[seed + 1][0].islower()):
            seed = random.randint(0, self.text_size - 4)
            if '.' in self.words[seed + 1]:
                seed = random.randint(0, self.text_size - 4)

        seed_word, next_word, next_next_word = self.words[
            seed], self.words[seed + 1], self.words[seed + 2]
        w1, w2, w3 = seed_word, next_word, next_next_word
        gen_words = []
        if w2.startswith("\""):
            inQuote = True

            
        for i in range(size):
            # Generate words for the quote until the quote is finished
            if inQuote:
                gen_words.append(w2)
                w1, w2, w3 = w2, w3, random.choice(self.cache[(w1, w2, w3)])

                # If you're already in a quote, don't generate the start of another one
                while w2.startswith("\""):
                    w1,w2,w3 = w2, w3, random.choice(self.cache[(w1, w2, w3)])

                # If there is an end quote mark while in a quote, end that quote
                if w2.strip().endswith("\""):
                    inQuote = False
                    gen_words.append(w2)
                    
            else:
                # If there is an end quote mark while not in a quote, generate new words
                while w2.strip().endswith("\"") and not inQuote:
                    w1, w2, w3 = w2, w3, random.choice(self.cache[(w1, w2, w3)])

                gen_words.append(w2)
                w1, w2, w3 = w2, w3, random.choice(self.cache[(w1, w2, w3)])

                

                # If there is a starting quote mark while not in a quote, start a quote
                if w2.startswith("\""):
                    inQuote = True

                # If there is an end of a sentence, start a new sentence
                if w3.strip().endswith(('.','!','?')):
                    break


        gen_words.append(w2)    
        gen_words.append(w3)

        return ' '.join(gen_words)
