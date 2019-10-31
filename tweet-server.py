"""
Sanic sever that tweets listens for permits and tweets them.
"""
from datetime import datetime
import json
import logging

from sanic import Sanic
from sanic import response
from sanic import exceptions
import twitter

from config.secrets import (
    CONSUMER_API_KEY,
    CONSUMER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    ENDPOINT,
    TOKEN
)

from config.config import BASE_URL

api = twitter.Api(
    consumer_key=CONSUMER_API_KEY,
    consumer_secret=CONSUMER_API_SECRET,
    access_token_key=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
)

app = Sanic()

def parse_subtype(subtype):
    # e.g. etxtract subtype description from something like `R- 101 Single Family Houses`
    subtype = subtype.replace('- ', '')
    subtype = subtype.split(' ')
    return ' '.join(subtype[1:])


def format_tweet(permit):
    return f"{permit['status']}: {permit['subtype']} at {permit['project_name']}. {BASE_URL}{permit['rsn']}"


@app.route("/tweet", methods=['POST'])
def post_json(request):
    permit = request.json
    subtype = permit["subtype"]
    permit["subtype"] = parse_subtype(subtype)
    tweet = format_tweet(permit)
    res = api.PostUpdate(tweet)
    return response.text(tweet)


@app.route("/")
async def index(request):
    now = datetime.now().isoformat()
    return response.text(f"Tweet server OK at {now}")


if __name__ == "__main__":
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=8000)