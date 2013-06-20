#!/usr/bin/env python
# -*- coding: utf-8 -*-


stopwords_esp = []
stopwords_eng = []

with open('spanish', 'r') as f:
    for line in f:
        stopwords_esp.append(line[:-1])

with open('english', 'r') as f:
    for line in f:
        stopwords_eng.append(line[:-1])
