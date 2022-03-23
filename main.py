import datetime
import collections
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
import argparse
from jinja2 import Environment, FileSystemLoader, select_autoescape

WINERY_FOUNDATION_YEAR = 1920


def pluralize(number, words):
    if all((number % 10 == 1, number % 100 != 11)):
        return words[0]
    elif all((2 <= number % 10 <= 4,
             any((number % 100 < 10, number % 100 >= 20)))):
        return words[1]
    return words[2]


args_parser = argparse.ArgumentParser()
args_parser.add_argument(
    '--path',
    help='Название xlsx файла',
    default='wine.xlsx'
)
args = args_parser.parse_args()

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')

current_year = datetime.datetime.today().year
winery_age = current_year - WINERY_FOUNDATION_YEAR

excel_wines_df = pandas.read_excel(
    args.path,
    na_values=None,
    keep_default_na=False
)
wines = excel_wines_df.to_dict(orient='records')
wines_by_categories = collections.defaultdict(list)

for wine in wines:
    wines_by_categories[wine['Категория']].append(wine)

rendered_page = template.render(
    winery_age=f'{winery_age} {pluralize(winery_age, ["год", "года", "лет"])}',
    wines_by_categories=wines_by_categories
)

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
