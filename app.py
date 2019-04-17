import utils.logit as logit
import re
from flask import Flask, jsonify
from infrastructure.html_table_parser import convert_html_table, extract_tables_from_html

app = Flask(__name__)


def scrape_licenses_from_wikipedia():
    url = 'https://en.wikipedia.org/wiki/Comparison_of_free_and_open-source_software_licenses'
    tables = extract_tables_from_html(url)
    if not tables:
        raise Exception("No tables found in {}".format(url))
    licenses = convert_html_table(tables[0])
    msg = f"Loaded {len(licenses)} Licenses from {url}"
    logit.log_info(msg)
    return licenses


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


licenses = scrape_licenses_from_wikipedia()
