import pandas as pd
import requests

from infrastructure.html_table_parser import get_all_tables_from_html


class HTMLTableParser:

    def extract_tables_from_html(self, url):
        try:
            response = requests.get(url)
            return get_all_tables_from_html(response.text)
        except Exception as e:
            raise e

    def html_table_to_dataframe(self, table):
        n_columns = 0
        n_rows = 0
        column_names = []
        for row in table.find_all('tr'):
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    n_columns = len(td_tags)
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        df = pd.DataFrame(columns=columns,
                          index=range(0, n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker, column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        return df
