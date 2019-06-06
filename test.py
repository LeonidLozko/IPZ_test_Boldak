import nltk
import numpy as np
import random
import warnings
import string  # to process standard python strings
# Из библиотеки scikit learn импортируйте векторизатор TFidf,
# чтобы преобразовать коллекцию необработанных документов в матрицу функций TF-IDF.
from sklearn.feature_extraction.text import TfidfVectorizer
# Также импортируйте модуль косинусного сходства из библиотеки scikit learn.
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')

f = open('chatbot.txt', 'r', errors='ignore')
raw = f.read()
raw = raw.lower()  # converts to lowercase
nltk.download('punkt')  # first-time use only
nltk.download('wordnet')  # first-time use only
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words

lemmer = nltk.stem.WordNetLemmatizer()
# WordNet - это семантически ориентированный словарь английского языка, включенный в NLTK.

# WordNet is a semantically-oriented dictionary of English included in NLTK.

# Теперь мы определим функцию под названием LemTokens,
# которая будет принимать в качестве входных токены и возвращать нормализованные токены
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]


def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def response(user_response):
    """Мы определяем ответ функции, который ищет в высказывании пользователя одно или несколько известных ключевых слов
     и возвращает один из нескольких возможных ответов. Если он не находит ввод, соответствующий какому-либо из
      ключевых слов, он возвращает ответ: «Извините! Я вас не понимаю"""
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        robo_response = robo_response + "I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response
