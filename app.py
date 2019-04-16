import json
import re
from flask import Flask, jsonify
from scrape_license_info import HTMLTableParser

app = Flask(__name__)

url = 'https://en.wikipedia.org/wiki/Comparison_of_free_and_open-source_software_licenses'
hp = HTMLTableParser()
table = hp.parse_url(url)
as_json = table.to_json(orient='records')
json_as_string = str(as_json).replace('\\n', '').replace('\\"', '').replace("'", "\"")
oss_dict = json.loads(json_as_string)


@app.route("/")
def say_hello():
    return jsonify({"message": "Hi I'm OSSI! The OSS License Checker!"})


@app.route('/licenses/<search>')
def search_license_by_string(search):
    for license_data in oss_dict:
        if re.match(search, license_data['License'], re.IGNORECASE):
            return jsonify(license_data)


@app.route('/licenses')
def get_all_licenses():
    return jsonify(oss_dict)
