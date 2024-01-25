import requests
from lxml import etree
import urllib3
from config import *
from flask import *

urllib3.disable_warnings()

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

def query(content, page):
    result = []
    content = content.replace(' ', '+')
    URL = f"{google_mirror}/search?q={content}&start={page}"
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(URL, headers = headers, verify = False)
    if resp.status_code == 200:
        tree = etree.HTML(resp.text)
        title = (tree.xpath('//*[@id="rso"]/div/div/div/div[1]/div/div/span/a/h3/text()') + tree.xpath('//*[@id="rso"]/div/div/div/div/div/div/div[1]/div[1]/div/div/span/a/h3/text()'))
        href = (tree.xpath('//*[@id="rso"]/div/div/div/div[1]/div/div/span/a/@href') + tree.xpath('//*[@id="rso"]/div/div/div/div/div/div/div[1]/div[1]/div/div/span/a/@href'))
        for i in range(len(title)):
            result.append({'title': title[i], 'href': href[i]})
    set_result = []
    for i in result:
        if i not in set_result:
            set_result.append(i)
    return set_result

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    content = request.values.get('query')
    page = request.values.get('page')
    if content is None:
        return redirect('/')
    if page is None:
        page = 1
    return render_template('search.html', results = query(content, page), page = page, query = content)
