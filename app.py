from flask import Flask, render_template, flash, request
import requests
from bs4 import BeautifulSoup
from scraper import *

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('home.html')


@app.route('/results')
def scraper():
    search = request.args.get('search_term')
    rmdcomp = search_mdcomputers(search)
    rkhrd = search_kharidiye(search)
    rprime = search_prime(search)

    return render_template('results.html', result_mdcomp=rmdcomp, result_khrd=rkhrd, result_prime=rprime)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()
