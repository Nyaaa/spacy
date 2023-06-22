from collections import defaultdict
from pprint import pprint
from loader import load_sample
import ru_core_news_sm
from spacy.lang.ru import stop_words
from spacy.matcher import Matcher
import timer


nlp = ru_core_news_sm.load()
nlp.enable_pipe("senter")
spacy_stopwords = stop_words.STOP_WORDS
matcher = Matcher(nlp.vocab)
loader = defaultdict(set)


CONF_DATE_PATTERNS = [
    [{"LEMMA": "состояться"}],
    [{"LEMMA": "открыться"}],
    [{"LEMMA": "открываться"}],
    [{"LEMMA": "пройти"}],
    [{"LEMMA": "дата"}],
    [{"LEMMA": "провести"}],
]
REG_DATE_PATTERNS = [
    [{"LEMMA": "заявка"}],
    [{"LEMMA": "приниматься"}],
    [{"LEMMA": "участиe"}],
    [{"LEMMA": "регистрация"}],
]
ADDRESS_PATTERNS = [
    [{"LEMMA": "место"}],
    [{"LEMMA": "адрес"}],
    [{"LEMMA": "город"}],
    [{"LEMMA": "гибридный"}],
    [{"LEMMA": "очный"}],
]
CONTACT_PATTERNS = [
    [{"LOWER": "тел."}],
    [{"LEMMA": "телефон"}],
    [{"LEMMA": "контакт"}],
    [{"LEMMA": "mail"}],
    [{"LEMMA": "почта"}],
    [{"LIKE_EMAIL": True}],
]
WOS_PATTERNS = [
    [{"LOWER": "wos"}],
    [{"LOWER": "web"}, {"LOWER": "of"}, {"LOWER": "science"}],
]
VAK_PATTERNS = [[{"ORTH": "ВАК"}]]
SCOPUS_PATTERNS = [[{"LOWER": "scopus"}]]
RINC_PATTERNS = [[{"LOWER": "ринц"}]]


@timer.wrapper
def nlp_parser():
    for line in load_sample():
        text = line.xpath("string(.)").get()
        doc = nlp(text)
        for sent in doc.sents:
            find_matches(sent)
    return loader


def find_matches(sent):
    matcher.add("reg_date", REG_DATE_PATTERNS, on_match=print_matches_get_sent)
    matcher.add("conf_date", CONF_DATE_PATTERNS, on_match=print_matches_get_sent)
    matcher.add("contacts", CONTACT_PATTERNS, on_match=print_matches_get_sent)
    matcher.add("wos", WOS_PATTERNS, on_match=print_matches_get_bool)
    matcher.add("vak", VAK_PATTERNS, on_match=print_matches_get_bool)
    matcher.add("scopus", SCOPUS_PATTERNS, on_match=print_matches_get_bool)
    matcher.add("rinc", RINC_PATTERNS, on_match=print_matches_get_bool)
    matcher.add("conf_address", ADDRESS_PATTERNS, on_match=print_matches_get_sent)
    matcher.add("offline", ADDRESS_PATTERNS, on_match=print_matches_get_bool)
    matcher(sent)


def print_matches_get_sent(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    string_id = nlp.vocab.strings[match_id]
    span = doc[start:end]
    loader[string_id].add(span.sent)


def print_matches_get_match(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    string_id = nlp.vocab.strings[match_id]
    loader[string_id].add(doc[start:end])


def print_matches_get_bool(matcher, doc, i, matches):
    match_id, _, _ = matches[i]
    string_id = nlp.vocab.strings[match_id]
    loader[string_id] = True


pprint(nlp_parser())
