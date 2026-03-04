from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import os

app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/interest", methods=["GET"])
def interest():
    keyword = request.args.get("keyword")
    geo = request.args.get("geo", "US")
    timeframe = request.args.get("timeframe", "now 7-d")

    if not keyword:
        return jsonify({"error": "keyword required"}), 400

    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)

    data = pytrends.interest_over_time()

    if data.empty:
        return jsonify({"error": "no data"}), 404

    values = data[keyword].tolist()

    return jsonify({
        "keyword": keyword,
        "geo": geo,
        "timeframe": timeframe,
        "values": values
    })