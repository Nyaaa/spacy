from loader import load_sample
import timer

import ru_core_news_sm
from spacy.lang.ru import stop_words
from spacy.matcher import Matcher
from nltk import tokenize
from textblob import TextBlob


nlp = ru_core_news_sm.load()
nlp.enable_pipe("senter")
spacy_stopwords = stop_words.STOP_WORDS
matcher = Matcher(nlp.vocab)


@timer.wrapper
def control():
    for line in load_sample():
        text = line.xpath("string(.)").get()
        sent = [text.split()]
        yield sent


@timer.wrapper
def textblob():
    for line in load_sample():
        text = TextBlob(line.xpath("string(.)").get())
        yield text.sentences


@timer.wrapper
def nlp_parser():
    for line in load_sample():
        text = line.xpath("string(.)").get()
        doc = nlp(text)
        for sent in doc.sents:
            # tokens = [token.lemma_ for token in sent if token not in spacy_stopwords]
            # print(tokens)
            find_matches(sent)
            yield sent


def print_matches_sent(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    string_id = nlp.vocab.strings[match_id]
    span = doc[start:end]
    sents = span.sent
    print(string_id, sents)


def print_matches_match(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    string_id = nlp.vocab.strings[match_id]
    span = doc[start:end]
    print(string_id, span)


def find_matches(sent):
    conf_date_patterns = [
        [{"LEMMA": "состояться"}],
        [{"LEMMA": "открыться"}],
        [{"LEMMA": "открываться"}],
        [{"LEMMA": "пройти"}],
        [{"LEMMA": "дата"}],
        [{"LEMMA": "провести"}],
    ]
    reg_date_patterns = [
        [{"LEMMA": "заявка"}],
        [{"LEMMA": "приниматься"}],
        [{"LEMMA": "участиe"}],
        [{"LEMMA": "регистрация"}],
    ]
    email_patterns = [[{"LIKE_EMAIL": True}]]

    matcher.add("reg_date", reg_date_patterns, on_match=print_matches_sent)
    matcher.add("conf_date", conf_date_patterns, on_match=print_matches_sent)
    matcher.add("email", email_patterns, on_match=print_matches_match)
    matcher(sent)


# print(list(control()))
print(list(nlp_parser()))
# print(list(textblob()))
