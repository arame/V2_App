from config import Hyper
import os

def main2():
    consumer_key = os.getenv('CONSUMER_KEY')
    go_path = os.getenv('GOPATH')
    print(f"consumer key = {consumer_key}")
    print(f"go path = {go_path}")

def main1():
    for k, v in os.environ.items():
        print(f'{k}={v}')

def main():
    consumer_key = Hyper.consumer_key
    consumer_secret = Hyper.consumer_secret
    access_token = Hyper.access_token
    access_token_secret = Hyper.access_token_secret

    print(f"consumer key = {consumer_key}")
    print(f"consumer secret = {consumer_secret}")
    print(f"access token = {access_token}")
    print(f"access token secret = {access_token_secret}")

if __name__ == "__main__":
    main()