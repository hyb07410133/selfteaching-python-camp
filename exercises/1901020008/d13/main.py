import requests
import pyquery
import logging
import matplotlib.pyplot as plt
from wxpy import *
from mymodule import stats_word
from os import path
cwd = path.abspath(path.dirname(__file__))
logging.basicConfig(
    format='file:%(filename)s|line:%(lineno)d|message: %(message)s', level=logging.DEBUG)
plt.rcParams['font.sans-serif'] = 'SimHei'
def get_article(url):
    r = requests.get(url)
    document = pyquery.PyQuery(r.text)
    return document('#js_content').text()

def generate_image(data,image_path):
    labels = [v[0] for v in data]
    widths = [v[1] for v in data]
    ypos = range(len(data))
    fig, ax = plt.subplots()
    ax.barh(ypos, widths)
    ax.set_ytichk(ypos)
    ax.invert_yaxis()
    ax.set_ylabel('关键字')
    ax.set_ylabel('词频')
    ax.set_ylabel('词频统计')
    fig.savefig(image_path,bbox_inches='tight')



def main():
    bot = Bot()
    friends = bot.friends()

    @bot.register(friends, SHARING)
    def handler(msg):
        try:
            logging.info('sharing url = %s', msg.url)
            article = get_article(msg.url)
            result = stats_word.stats_text_cn(article, 20)
            image_path = path.join(cwd, 'stats.png')
            generate_image(result,image_path)
            msg.reply_image(image_path)
        except Exception as e:
            logging.exception(e)
    embed()

if __name__ == "__main__":
  main()