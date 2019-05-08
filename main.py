import os
import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()

def get_fact():
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


def get_pig_latin(fact):
    page = """
<table>
    <tr><th>Fact from unkno.com:</th><td>{}</td></tr>
    <tr><th>URL from pig latinizer:</th><td>{}</td></tr>
</table>
-------------------------------------------------------------
<table>
    <tr><th>Response from pig latinizer:</th><td>{}</td></tr>
</table>
"""

    this_url = 'https://hidden-journey-62459.herokuapp.com/piglatinize/'
    this_data = {"input_text":fact}

    response = requests.post(url=this_url, data=this_data)
    
    return page.format(fact, response.url, response.text)

@app.route('/')
def home():
    this_fact = get_fact()
    return get_pig_latin(this_fact)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
