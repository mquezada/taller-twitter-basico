#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.corpus import stopwords
import unicodedata
import re

tco_urls_pattern = re.compile("(https?:\/\/.*?/[a-zA-Z0-9]*)")


def remove_diacritic(input):
    try:
        return unicodedata.normalize('NFKD', input).encode('ASCII', 'ignore')
    except:
        return ''


def clean_words(text, lang='spanish'):
    text = remove_diacritic(text)  # removes diacritics (acentos)
    text = tco_urls_pattern.sub('', text)  # removes urls from t.co
    words = re.findall(r'\w+', text, flags=re.UNICODE | re.LOCALE)  # tokenize, removes punctuation
    #words = text.split()
    return [word.lower() for word in words if len(word) >= 3 and word not in stopwords.words(lang)]
