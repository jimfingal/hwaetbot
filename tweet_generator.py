import random

from markov import MarkovChain

UTF8_TAB = '\xc2\xa0'

class TweetGenerator(object):
    
    def __init__(self, riddle_sentences, ngram_size):
        
        self.riddle_sentences = set(riddle_sentences)
        self.chain = MarkovChain(ngram_size=ngram_size)
        
        for sentence in self.riddle_sentences:
            self.chain.train_sentence(sentence)
    
    def get_unique_sentence(self):
        while True:
            s = self.chain.generate_sentence()
            if s.lower() not in self.riddle_sentences:
                break
        return s


    def generate_tweet(self):
        tweet = ''

        while True:
            next_sentence = self.get_unique_sentence()
            if len(next_sentence) > 125:
                continue
            if len(tweet) > 0 and len(tweet) + len(next_sentence) > 125:
                break
            tweet = tweet + next_sentence + ' '

        return tweet[:-1].strip()



if __name__ == "__main__":
    from parse_riddles import parse_corpus

    corpus = parse_corpus()

    tg = TweetGenerator(corpus, 3)

    for i in range(0, 100):
        print "%s :: %s" % (i, tg.generate_tweet())


def fake_anglo_saxon_meter(sentence):
    new_sentence = ''
    split_sentence = sentence.split(' ')
    while len(split_sentence) > 0:
        first_half = random.randrange(3, 5)
        second_half = 4 if first_half == 3 else 3    
        new_sentence = new_sentence + ' '.join(split_sentence[:first_half]) + 4 * UTF8_TAB + \
            ' '.join(split_sentence[first_half:first_half + second_half]) + '\n' 
        split_sentence = split_sentence[first_half + second_half:]
    return new_sentence.strip().strip(UTF8_TAB)