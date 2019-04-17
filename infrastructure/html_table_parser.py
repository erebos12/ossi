from bs4 import BeautifulSoup

def get_all_tables_from_html(html):
    try:
        soup = BeautifulSoup(html, 'lxml')
        return list(soup.find_all('table'))
    except Exception as e:
        raise e
