from bs4 import BeautifulSoup
import requests
import safer
import yaml

SHIELDS_URL = 'https://shields.io'
FILE = 'shields.yml'
INTERMEDIATE_FILE = 'shields-inter.yml'


def get_soup(url=''):
    page = requests.get(SHIELDS_URL + url)
    return BeautifulSoup(page.text, features='html.parser')


def get_categories():
    soup = get_soup()
    links = [a.get('href') for a in soup.find_all('a')]
    return sorted(i for i in links if i.startswith('/category'))


def get_shield_template(category):
    for row in get_soup(category).find('table').find('tbody').find_all('tr'):
        yield row.find('th').text.rstrip(':'), row.find('code').text


def scrape_all_shields():
    results = {}

    for category in get_categories():
        name = category.split('/')[-1]
        results[name] = result = {}
        for name, template in get_shield_template(category):
            result[name] = template

    return results


def get_all_shields():
    with open(INTERMEDIATE_FILE) as fp:
        return yaml.safe_load(fp)


def re_key(shields):
    result = {}

    for category, items in shields.items():
        for alt, item in items.items():
            blank, root, *rest = item.split('/', maxsplit=2)
            assert not blank, blank
            url = rest[0] if rest else ''
            result.setdefault(root, []).append([alt, url, category])

    return result


def print_re_key(shields):
    with safer.printer(FILE) as print:
        first = True
        for root, items in sorted(shields.items()):
            if first:
                first = False
            else:
                print()
            print('%s:' % root)
            for alt, url, category in sorted(items):
                print("- ['%s', '%s', '%s']" % (url, alt, category))


def main():
    scraped = scrape_all_shields()
    print_re_key(re_key(scraped))


if __name__ == '__main__':
    main()
