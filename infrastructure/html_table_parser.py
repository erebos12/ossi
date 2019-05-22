from bs4 import BeautifulSoup
import requests


def extract_tables_from_html(url):
    try:
        response = requests.get(url)
        return get_all_tables_from_html(response.text)
    except Exception as e:
        raise e


def get_all_tables_from_html(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        return list(soup.find_all('table'))
    except Exception as e:
        raise e


def convert_html_table(html_table):
    table_as_dict_list = []
    header_list = []
    for row in html_table.find_all('tr'):
        if not header_list:
            header_list = __get_header_data(row)
        items = __get_row_data(row)
        if (items and header_list) and (len(items) == len(header_list)):
            table_as_dict_list.append(__zip_it(header_list, items))
    return table_as_dict_list


def __get_row_data(html_row):
    data = html_row.find_all('td')
    return __get_data_as_list(data)


def __get_header_data(html_row):
    headers = html_row.find_all('th')
    return __get_data_as_list(headers)


def __get_data_as_list(data):
    return [str(d.get_text()).rstrip() for d in data if d.get_text()]


def __zip_it(keys, values):
    return dict(zip(keys, values))
