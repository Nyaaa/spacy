from loader import load_sample
import timer

import ru_core_news_sm
from spacy.lang.ru import stop_words
from spacy.matcher import Matcher
from spacy.tokens import Span


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
def nlp_parser():
    for line in load_sample():
        text = line.xpath("string(.)").get()
        doc = nlp(text)
        for sent in doc.sents:
            tokens = [token for token in sent if token not in spacy_stopwords]
            has_dates(sent)
            yield tokens


def print_matches(matcher, doc, i, matches):
    # Get the current match and create tuple of entity label, start and end.
    # Append entity to the doc's entity. (Don't overwrite doc.ents!)
    match_id, start, end = matches[i]
    entity = Span(doc, start, end, label="EVENT")
    doc.ents += (entity,)
    print(nlp.vocab.strings[match_id], doc)


def has_dates(sent):
    patterns = [
        [{"TEXT": {"REGEX": "состо[ия]тся"}}],
        [{"LOWER": "открытие"}],
        [{"LOWER": "проведен"}],
        [{"LOWER": "дата"}],
        [{"LOWER": "пройд"}],
        [{"TEXT": {"REGEX": "про[хв]од"}}],
    ]
    matcher.add("conf_date", patterns, on_match=print_matches)
    matcher(sent)


print(list(control()))
print(list(nlp_parser()))
