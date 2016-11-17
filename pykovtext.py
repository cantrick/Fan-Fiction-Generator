# Python markov chain text generator

import random


class Pykvtxt(object):

    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.parse_file()
        self.text_size = len(self.words)
        self.database()

    def parse_file(self):
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

    def printText(self, size=200):
        

        # Number of sentences to generate, and count for later loop

        
        seed = random.randint(0, self.text_size - 4)
        # Start sentence with a capital word so it looks like a real sentence
        while(self.words[seed + 1][0].islower()):
            seed = random.randint(0, self.text_size - 4)

        seed_word, next_word, next_next_word = self.words[
            seed], self.words[seed + 1], self.words[seed + 2]
        w1, w2, w3 = seed_word, next_word, next_next_word
        gen_words = []

            
        for i in range(size):
            gen_words.append(w2)
            w1, w2, w3 = w2, w3, random.choice(self.cache[(w1, w2, w3)])
            if w3.endswith(('.','!','?')):
                print("OK, ", w1, w2, w3)
                break
        gen_words.append(w2)    
        gen_words.append(w3)

        return ' '.join(gen_words)
