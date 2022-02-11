from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def pluralize(number, words):
    if all((number % 10 == 1, number % 100 != 11)):
        return words[0]
    elif all((2 <= number % 10 <= 4,
             any((number % 100 < 10, number % 100 >= 20)))):
        return words[1]
    return words[2]


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')

today = datetime.datetime.today()
winery_foundation_date = datetime.datetime(year=1920, month=1, day=1)
delta = today - winery_foundation_date
winery_age = delta.days // 365

excel_wines_df = pandas.read_excel('wine.xlsx')
wines = excel_wines_df.to_dict(orient='records')

rendered_page = template.render(
    winery_age=f'{winery_age} {pluralize(winery_age, ["год", "года", "лет"])}',
    wines=wines
)

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
