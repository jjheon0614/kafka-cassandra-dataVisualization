import asyncio
import configparser
import os
import time
from collections import namedtuple
from kafka import KafkaProducer
from faker import Faker
import json
import ccxt
from datetime import datetime

with open("api.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret
})

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))



def fetch_crypto_prices():
    # Get the current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Specify the trading pair symbols for Bitcoin, Ethereum, and Dogecoin against USDT
    symbols = ['BTC/USDT', 'ETH/USDT', 'DOGE/USDT']

    # Fetch ticker information for the specified trading pairs
    tickers = binance.fetch_tickers(symbols)

    crypto_prices = {}
    for symbol, ticker in tickers.items():
        # Extract the base symbol (e.g., 'BTC', 'ETH', 'DOGE')
        base_symbol = symbol.split('/')[0].lower()
        crypto_prices[base_symbol] = ticker['last']

    # Add a common 'time' key with the current timestamp
    crypto_prices['time'] = current_time

    return crypto_prices

    


def run():
    iterator = 0
    print("Setting up Crypto producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # Encode all values as JSON
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

    while True:
        crypto_prices = fetch_crypto_prices()

        # adding prints for debugging in logs
        print(f"Sending new crypto data iteration - {iterator}")
        producer.send(TOPIC_NAME, value=crypto_prices)
        print("New crypto data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1



if __name__ == "__main__":
    run()
