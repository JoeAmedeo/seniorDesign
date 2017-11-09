from flask import Flask
from url_documentation import URLDocumentation

app = Flask(__name__)
url_doc = URLDocumentation()

@url_doc.route('/', 'this prints out hello')
@app.route('/')
def index():
    return 'hello'

@url_doc.route('/site-map', 'this prints out the function of each URL defined in flask by app.route')
@app.route('/site-map')
def site_map():
    return url_doc.get_doc_string()

