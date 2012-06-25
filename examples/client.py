import requests
from requests.auth import OAuth1
from flask import Flask, redirect, request, session
from urlparse import parse_qsl, urlparse

app = Flask(__name__)
app.secret_key = "not very secret"
# TODO: read client key + secret from some config


@app.route("/start")
def start():
    client = OAuth1(u"gYMw03rEFMmaK2g18usXfpUw5awjcH", 
        client_secret=u"AUMLINSKDHwWJqwvVp7u1DmTznQhhV",
        callback_uri=u"http://127.0.0.1:5001/callback")
    r = requests.post(u"http://127.0.0.1:5000/request_token?realm=secret", auth=client)
    print r.content
    data = dict(parse_qsl(r.content))
    resource_owner = data.get(u'oauth_token')
    session["token_secret"] = data.get('oauth_token_secret').decode(u'utf-8')
    # TODO: store secret
    url = u"http://127.0.0.1:5000/authorize?oauth_token=" + resource_owner
    return redirect(url)


@app.route("/callback")
def callback():
    # Extract parameters from callback URL
    data = dict(parse_qsl(urlparse(request.url).query))
    resource_owner = data.get(u'oauth_token').decode(u'utf-8')
    verifier = data.get(u'oauth_verifier').decode(u'utf-8')
    token_secret = session["token_secret"]

    # Request the access token
    # TODO: use secret when fetching access token
    client = OAuth1(u"gYMw03rEFMmaK2g18usXfpUw5awjcH",
        client_secret=u"AUMLINSKDHwWJqwvVp7u1DmTznQhhV",
        resource_owner_key=resource_owner,
        resource_owner_secret=token_secret,
        verifier=verifier)
    print "USING SECRET::", token_secret
    r = requests.post(u"http://127.0.0.1:5000/access_token", auth=client)

    # Extract the access token from the response
    data = dict(parse_qsl(r.content))
    resource_owner = data.get(u'oauth_token').decode(u'utf-8')
    resource_owner_secret = data.get(u'oauth_token_secret').decode(u'utf-8')
    print data
    client = OAuth1(u"gYMw03rEFMmaK2g18usXfpUw5awjcH",
            client_secret=u"AUMLINSKDHwWJqwvVp7u1DmTznQhhV",
            resource_owner_key=resource_owner,
            resource_owner_secret=resource_owner_secret)
    print "SUPER SECRET::", resource_owner_secret
    r = requests.get(u"http://127.0.0.1:5000/protected", auth=client)
    print r.content
    r = requests.get(u"http://127.0.0.1:5000/protected_realm", auth=client)
    print r.content
    return r.content


if __name__ == "__main__":
    app.run(debug=True, port=5001)