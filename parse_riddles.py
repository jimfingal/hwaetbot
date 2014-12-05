import nltk
from bs4 import BeautifulSoup
from unipath import Path
import re

nltk.download('punkt', './nltk_data')
nltk.data.path.append('./nltk_data/')

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

UTF8_TAB = '\xc2\xa0'


p = Path('./riddlescrape/data/')
    
prose = []
english_riddles = []
old_english_riddles = []
for path in p.walk(filter=lambda p: p.isfile() and re.match(r".*html", p.name)):
    soup = BeautifulSoup(path.read_file().decode('utf-8'))
    prose = prose + [tag.text for tag in soup.select('div.prose p')]
    for row in soup.select("table tr"):
        row_tds = row.findAll('td', {'align': 'left'})
        if len(row_tds) > 1:
            english_riddles.append(row_tds[0].text.strip().encode('utf-8'))
            old_english_riddles = old_english_riddles + [tag.text.strip().encode('utf-8') for tag in row_tds[1:]]

print len(prose)
print len(english_riddles)
print len(old_english_riddles)


english_riddles[-1] = english_riddles[-1].replace(' (etc. as l. 2 above)', '') # Very specific fix

riddle_sentences = []

multiple_spaces = re.compile(ur'(\s)+', re.UNICODE)
space_before_punct = re.compile(ur' (\W)', re.UNICODE)

for riddle in english_riddles:
    sentences = sent_detector.tokenize(riddle.strip().decode('utf-8'))
    sentences = map(lambda x : x.encode('utf-8'), sentences)
    only_real_sentences = filter(lambda x: len(x) >= 15, sentences)
    cleaned = map(lambda x: re.sub(multiple_spaces, ' ', x.lower().replace('\n', ' ').replace('\xc2\xa0', ' ')), only_real_sentences)
    cleaned = map(lambda x: re.sub(space_before_punct, r'\1', x), cleaned)

    riddle_sentences = riddle_sentences + cleaned