from flask import Flask, render_template, request
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
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic.upper())
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def display_news(list_of_news, news_quantity):
    c = 1
    response = []
    for news in list_of_news:
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            print("Error:", e)

        news_id = str(c) + 'NewsBits'
        news_title = news.title.text
        news_summery = news_data.summary
        news_source = news.source.text
        news_link = news.link.text
        news_date = news.pubDate.text
        news_image = news_data.top_image

        data_dict = {}
        data_dict["news_id"] = news_id
        data_dict["news_title"] = news_title
        data_dict["news_image"] = news_image
        data_dict["news_summery"] = news_summery
        data_dict["news_source"] = news_source
        data_dict["news_link"] = news_link
        data_dict["news_date"] = news_date

        response.append(data_dict)

        print(f"Fetched News {c}")

        if c >= news_quantity:
            break
        c += 1

    return response


app = Flask(__name__)

default_news_quantity = 2


@app.route('/', methods=["GET","POST"])
def home_page():
    if request.method == "GET":
        print("GET '/'")
        news_list = fetch_top_news()
        response = display_news(list_of_news=news_list,
                                news_quantity=default_news_quantity)
        return render_template('home.html', response=response, topic="Top Trending", news_quantity=default_news_quantity, request_url="/")

    if request.method == "POST":
        load_more_range = int(request.form.get('load_more_range'))
        print(f"Loading more on '/' with news quantity: {load_more_range}")
        news_list = fetch_top_news()
        response = display_news(list_of_news=news_list,
                                news_quantity=load_more_range)
        return render_template('home.html', response=response, topic="Top Trending", news_quantity=load_more_range, request_url="/")


@app.route('/topics/<string:topic>', methods=["GET", "POST"])
def search_by_topics(topic):
    news_list = fetch_category_news(topic)
    if request.method == "GET":
        print(f"GET '/topics/{topic}'")
        response = display_news(list_of_news=news_list,
                                news_quantity=default_news_quantity)
        return render_template('home.html', response=response, topic=topic.upper(), news_quantity=default_news_quantity, request_url="/topics/"+topic)

    if request.method == "POST":
        load_more_range = int(request.form.get('load_more_range'))
        print(f"Loading more on '/topics/{topic}' with news quantity: {load_more_range}")
        response = display_news(list_of_news=news_list,
                                news_quantity=load_more_range)
        return render_template('home.html', response=response, topic=topic.upper(), news_quantity=load_more_range, request_url="/topics/"+topic)


@app.route('/search', methods=["GET","POST"])
def search():
    if request.method == "GET":
        print("GET '/search'")
        return render_template('home.html', request_url="/search")

    if request.method == "POST":
        try:
            load_more_range = int(request.form.get('load_more_range'))
        except:
            load_more_range = default_news_quantity
        topic = request.form.get('topic')
        print(f"Searching for {topic} with news quantity: {load_more_range}")
        news_list = fetch_news_search_topic(topic)
        response = display_news(list_of_news=news_list,
                                news_quantity=load_more_range)
        return render_template('home.html', response=response, topic=topic, news_quantity=load_more_range, request_url="/search")


# if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=3000,debug=True)