from flask import Flask, render_template, request
import requests
import re
from datetime import datetime
import csv

app = Flask(__name__)

key = "QNBSQ569PDAHAV41"
symbols_file = "stocks.csv"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_symbol = request.form['symbol']
        user_time = request.form['time']
        user_start = request.form['start_date']
        user_end = request.form['end_date']
        chart_type = request.form['chart_type']


        data = get_data(user_symbol, user_time, user_start, user_end)
        return render_template('index.html', data=data)

    symbols = get_symbols()
    return render_template('index.html', symbols=symbols)


def get_symbols():
    symbols = []
    with open(symbols_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            symbols.append(row['Symbol'])
    return symbols


def get_data(symbol, time, start, end):
    time_series_options = ["TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY"]

    url = f'https://www.alphavantage.co/query?function={time_series_options[int(time) - 1]}&symbol={symbol}&interval=5min&apikey={key}'
    
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return data
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
