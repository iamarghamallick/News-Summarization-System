from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article


def fetch_news_search_topic(topic):
    site = 'https://news.google.com/rss/search?q={}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def display_news(list_of_news, news_quantity):
    c = 0
    for news in list_of_news:
        c += 1
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            print("Error:", e)

        news_title = news.title.text
        news_image = news_data.top_image
        news_summery = news_data.summary
        news_source = news.source.text
        news_link = news.link.text
        news_date = news.pubDate.text

        if c >= news_quantity:
            break

if __name__ == "__main__":
    news_list = fetch_top_news()
    display_news(list_of_news=news_list, news_quantity=1)