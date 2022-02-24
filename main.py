import re

import requests

from bs4 import BeautifulSoup

import argparse


def create_file(word):
    file_name = word + '.txt'
    return open(file_name, 'a', encoding='utf-8')


def gen_url(word, input_lang, trans_lang):
    return 'https://context.reverso.net/translation/{}-{}/{}'.format(input_lang, trans_lang, word)


def display_translation(ln, translation):
    print(ln.capitalize() + ' Translations:')
    print(translation[1])


def write_translation(ln, translation, file):
    file.write(ln.capitalize() + ' Translations:\n')
    file.write(translation[1] + '\n')


def display_example(ln, example):
    print('\n' + ln.capitalize() + ' Examples:')
    print(example[0])
    print(example[1] + '\n\n')


def write_example(ln, example, file):

    file.write('\n' + ln.capitalize() + ' Examples:\n')
    file.write(example[0] + '\n')
    file.write(example[1] + '\n\n\n')


def translator(url_):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        page = requests.get(url_, headers=headers)
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
    except requests.exceptions.InvalidSchema:
        print('Sorry, unable to find', trans_word)
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        t2 = soup.find_all(class_='translation', limit=2)
        d = soup.find_all('div', class_=re.compile('src|trg'), limit=2)
        try:
            message2 = 'Sorry, unable to find '
            assert len(t2) > 1, message2 + trans_word
        except AssertionError as er:
            print(er)
        else:
            translations = []
            description = []
            for tr in t2:
                if len(tr):
                    translations.append(tr.text.strip())

            for dr in d:
                txt = " ".join(dr.text.split())
                if len(txt) > 1:
                    description.append(txt)
            file = create_file(trans_word)
            display_translation(lang2, translations)
            write_translation(lang2, translations, file)
            display_example(lang2, description)
            write_example(lang2, description, file)
            file.close()


lang = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese',
        'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish']

parser = argparse.ArgumentParser()
parser.add_argument("l1")
parser.add_argument("l2")
parser.add_argument("w")
args = parser.parse_args()


try:
    message = "Sorry, the program doesn't support "
    assert args.l1 in lang, message + args.l1
    assert args.l2 in lang or args.l2 == 'all', message + args.l2
except AssertionError as err:
    print(err)

lang1 = args.l1
opt2 = args.l2
trans_word = args.w

if opt2 != 'all':
    lang2 = opt2
    url = gen_url(trans_word, lang1, lang2)
    translator(url)
else:
    for language in lang:
        lang2 = language
        if lang2 != lang1:
            url = gen_url(trans_word, lang1, lang2)
            translator(url)

# command line args to tests the script
# python main.py english all test
