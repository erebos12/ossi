import os
import unittest

from infrastructure.html_table_parser import get_all_tables_from_html, convert_html_table


def get_html_from_file(filename):
    try:
        file = open(os.path.abspath(filename), 'r')
        return file.read()
    finally:
        file.close()


class TestParseHTMLTable(unittest.TestCase):

    def test_simple_table(self):
        html = get_html_from_file('sample_html_table.html')
        table = get_all_tables_from_html(html)
        self.assertIsNotNone(table)

    def test_parse_html_table(self):
        html = get_html_from_file('sample_html_table.html')
        tables = get_all_tables_from_html(html)
        tbl_as_dict_list = convert_html_table(tables[0])
        self.assertEqual(2, len(tbl_as_dict_list))
        self.assertEqual("Jill", tbl_as_dict_list[0]['Firstname'])
        self.assertEqual("Eve", tbl_as_dict_list[1]['Firstname'])
        self.assertEqual("Smith", tbl_as_dict_list[0]['Lastname'])
        self.assertEqual("Jackson", tbl_as_dict_list[1]['Lastname'])
