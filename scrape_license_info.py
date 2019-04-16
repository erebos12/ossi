import requests
from bs4 import BeautifulSoup as soup

url = 'https://en.wikipedia.org/wiki/Comparison_of_free_and_open-source_software_licenses'

raw_html = requests.get(url).text

html = soup(raw_html, 'lxml')

table = soup.find_all(html)[0]  # Grab the first table

output_rows = []
for table_row in table.findAll('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    output_rows.append(output_row)

print(output_rows)
