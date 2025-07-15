from flask import Flask, request, render_template
from scraper import scrape_okru

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    urls = ""
    if request.method == 'POST':
        urls = request.form.get('urls') or ""
        url_list = [u.strip() for u in urls.splitlines() if u.strip()]
        for url in url_list:
            result = scrape_okru(url)
            result['url'] = url
            results.append(result)
    return render_template('index.html', results=results, urls=urls)

if __name__ == '__main__':
    app.run(debug=True)