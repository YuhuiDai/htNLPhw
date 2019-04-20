from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import re
from bs4 import BeautifulSoup
import urllib3


class TextExtractor():
    # https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text/1983219#1983219

    def __init__(self, url, local=True):
        self.http = urllib3.PoolManager()
        r = self.http.request('GET', url)
        html_str = r.data.decode('utf-8')
        self.data = BeautifulSoup(html_str, 'html5lib').findAll(text=True)

    def visible(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'li', 'ul', 'button']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True

    def getText(self):
        text = filter(self.visible, self.data)
        result = ''
        for line in list(text):
            if len(line.split()) > 0:
                result += line.strip()
                result += ' '
        return result

def sentiment_analysis(text):
    sia = SIA()
    score = sia.polarity_scores(text)
    print(score)
    overall = score['compound']
    negative = score['neg']
    positive = score['pos']
    neutral = score['neu']
    return overall, negative, positive, neutral

def example_sentiment_analysis(url):
    te = TextExtractor(url, local=False)
    print(sentiment_analysis(te.getText()))


if __name__ == '__main__':
    url = 'https://www.cnn.com'
    example_sentiment_analysis(url)

