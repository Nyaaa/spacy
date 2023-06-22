from loader import load_sample
import timer
from textblob import TextBlob


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


print(list(control()))
print(list(textblob()))
