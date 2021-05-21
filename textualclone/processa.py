import json
from pprint import pprint
import string
import sys
import unicodedata

from bs4 import BeautifulSoup
from bs4.element import Comment

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import *

import nltk
#nltk.download('punkt')
#nltk.download('rslp')


def replace_ptbr_char_by_word(word):
    word = str(word)
    word = unicodedata.normalize('NFKD', word).encode('ASCII','ignore').decode('ASCII')
    return word

stemmer = nltk.stem.RSLPStemmer()
stopwords = [replace_ptbr_char_by_word(stemmer.stem(item.lower())) for item in nltk.corpus.stopwords.words('portuguese')] + \
    nltk.corpus.stopwords.words('portuguese') + \
    [stemmer.stem(item.lower()) for item in nltk.corpus.stopwords.words('portuguese')] + \
    ['fo', 'es', 'estav', 'estives', 'fos', 'houveri', 'houves', 'is', 'sera', 'seri', 'tamb', 'tera', 'teri', 'tives']

remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

cache = {}

def cache_steam(item):
    if item not in cache:
        result = stemmer.stem(item)
        cache[item] = result
    return cache[item]


def normalize(text):
    tokens = nltk.word_tokenize(replace_ptbr_char_by_word(text.lower()))
    return [cache_steam(item) for item in tokens]

def cosine_sim(texts):
    tf_idf = TfidfVectorizer(max_df=0.99, strip_accents='ascii', tokenizer=normalize, stop_words=stopwords).fit_transform(texts)
    return cosine_distances(tf_idf)

def text_from_html(body):
    soup = BeautifulSoup(body, 'lxml')
    texts = soup.findAll(text=True)
    return u" ".join(t.strip() for t in texts if t.strip())

def process_questions():
    q_id_file = sys.argv[1]
    questions = {}
    for question in json.loads(open(q_id_file).read()):
        questions[question['id']] = (text_from_html(question['question_text']))
    return questions

def process_submissions():
    s_id_file = sys.argv[2]
    submissions = {}
    for submission in json.loads(open(s_id_file).read()):
        if not 'submission_data' in submission['submission_history'][-1]:
            continue
        user_id = submission['user_id']
        submission_data = submission['submission_history'][-1]['submission_data']
        for sub_awnser in submission_data:
            answers = submissions.setdefault(user_id, {})
            answers[sub_awnser["question_id"]] = text_from_html(sub_awnser['text'])
    return submissions

def process_sim(questions, submissions):
    sim_matrix = []
    for q_id in questions.keys():
        users = []
        texts = []
        for u_id, answers in submissions.items():
            if q_id not in answers or not answers[q_id] or not answers[q_id].strip():
                continue
            users.append(u_id)
            texts.append(answers[q_id])
        if not users or not texts:
            continue
        sim = cosine_sim(texts)
        for c1, u1 in enumerate(users):
            for c2, u2 in enumerate(users[c1 + 1:]):
                sim_matrix.append([sim[c1][c1 + 1 + c2],
                                    q_id,
                                    u1,
                                    u2,
                                    texts[c1],
                                    texts[c1 + 1 + c2]])
    return sim_matrix


questions = process_questions()
submissions = process_submissions()

sim_matrix = process_sim(questions, submissions)

total = 0
alunos = set()

for x in sorted(sim_matrix, key=lambda x:x[0]):
    if x[1] in [105051165, 105051166, 105051169]:
        continue
    if x[0] < 0.1:
        print(x[0], x[1], x[2], x[3])
        alunos.add(x[2])
        alunos.add(x[3])
        print("X[1]", x[1])
        print("---")
        print("X[4]", x[4])
        print("---")
        print("X[5]", x[5])
        print("=========")
        total += 1

print(total)
print(alunos)