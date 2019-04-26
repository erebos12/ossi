import utils.logit as logit
import re
from flask import Flask, jsonify, Blueprint
from flask_restplus import Api, Resource
from infrastructure.html_table_parser import convert_html_table, extract_tables_from_html

flask_app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
app = Api(app=flask_app,
          version='1.0',
          title='OSSI',
          description='OSSI - OSS Licence Checker',
          doc='/swagger')

name_space = app.namespace('OSSI', description='OSSI APIs')


def scrape_licenses_from_wikipedia():
    url = 'https://en.wikipedia.org/wiki/Comparison_of_free_and_open-source_software_licenses'
    tables = extract_tables_from_html(url)
    if not tables:
        raise Exception("No tables found in {}".format(url))
    licenses = convert_html_table(tables[0])
    msg = f"Loaded {len(licenses)} Licenses from {url}"
    logit.log_info(msg)
    return licenses


@app.route("/healthz")
class OssiHello(Resource):
    def get(self):
        """
        Say hello
        """
        return jsonify({"message": "Hi I'm OSSI!"})


@app.route("/licenses/<search>")
class OssiLicensesSearch(Resource):
    def get(self, search):
        """
        Search for a license by a string
        """
        result = [license for license in licenses if re.match(search, license['License'], re.IGNORECASE)]
        return jsonify(result) if result else jsonify({"message": "Nothing found for {}".format(search)})


@app.route("/licenses")
class OssiLicenses(Resource):
    def get(self):
        """
        Get all license info
        """
        return jsonify(licenses)


licenses = scrape_licenses_from_wikipedia()
