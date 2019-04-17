import os
import unittest

from infrastructure.html_table_parser import get_all_tables_from_html
from infrastructure.scrape_license_info import HTMLTableParser


def get_html_from_file(filename):
    try:
        file = open(os.path.abspath(filename), 'r')
        return file.read()
    finally:
        file.close()


class TestParseHTMLTable(unittest.TestCase):
    parser = HTMLTableParser()

    def test_simple_table(self):
        html = get_html_from_file('sample_html_table.html')
        table = get_all_tables_from_html(html)
        self.assertIsNotNone(table)

    def test_with_complex_parser(self):
        html = get_html_from_file('sample_html_table.html')
        tables = get_all_tables_from_html(html)
        self.assertEqual(1, len(tables))
        table_as_df = self.parser.html_table_to_dataframe(tables[0])
        self.assertIsNotNone(table_as_df)
        self.assertEqual(2, len(table_as_df))
        self.assertEqual("Jill", table_as_df['Firstname'].iloc[0])
        self.assertEqual("Eve", table_as_df['Firstname'].iloc[1])
        self.assertEqual("Smith", table_as_df['Lastname'].iloc[0])
        self.assertEqual("Jackson", table_as_df['Lastname'].iloc[1])
