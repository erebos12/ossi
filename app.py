import json
import re
from flask import Flask, jsonify
from infrastructure.scrape_license_info import HTMLTableParser

app = Flask(__name__)

url = 'https://en.wikipedia.org/wiki/Comparison_of_free_and_open-source_software_licenses'
hp = HTMLTableParser()
tables = hp.extract_tables_from_html(url)
if not tables:
    raise Exception("No tables found in {}".format(url))

table = hp.html_table_to_dataframe(tables[0])  # take the first table
as_json = table.to_json(orient='records')
json_as_string = str(as_json).replace('\\n', '').replace('\\"', '').replace("'", "\"")
licenses = json.loads(json_as_string)


@app.route("/")
def say_hello():
    return jsonify({"message": "Hi I'm OSSI! The [OSS] L[I]cense Checker!"})


@app.route('/licenses/<search>')
def search_license_by_string(search):
    for license in licenses:
        if re.match(search, license['License'], re.IGNORECASE):
            return jsonify(license)
    return jsonify({"message": "Nothing found for {}".format(search)})


@app.route('/licenses')
def get_all_licenses():
    return jsonify(licenses)
