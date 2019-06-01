# coding=utf-8
# macos: python3 app.py

import requests
import time
import pandas as pd
import itertools
from pprint import pprint

print('app is started')

#1. API Prozorro.gov.ua
# Посилання: https://prozorro.gov.ua/
# Документація: https://prozorro.gov.ua/openprocurement
# Модуль аналітики: https://bi.prozorro.org/

# Завдання #1: ознайомитись з даними Prozorro
# отримаємо перелік тендерів з системи
tender_list = requests.get("https://public.api.openprocurement.org/api/2.5/tenders").json()
pprint(tender_list)

# отримаємо тендер за ідентифікатором
# переглянути тендер у веб: https://prozorro.gov.ua/tender/UA-2019-05-28-001297-a
tender = requests.get("https://public.api.openprocurement.org/api/2.5/tenders/41a2ea0d76604c7198a333fc382f30e6").json()
pprint(tender)

#2. API Clarity-project.info
# Посилання: https://clarity-project.info/tenders
# Документація: https://github.com/the-clarity-project/api/blob/master/README.md
# Суперсила: фактори ризику в закупівлях, API до ЄДР
#
# Завдання #2: Вивести перелік тендерів з найвищими корупційними ризиками
# запит:
# entity=03365245 | (Головне управління ЖКГ міcької ради міста Кропивницького)
# date_from=01-01-2019 & date_to=01-06-2019 | (півріччя 2019)
# status=complete & method=open | (завершені конкурентні торги)
# увага clarity віддає по 100 записів

tenders = requests.get("https://clarity-project.info/api/tender.search?entity=03365245&date_from=01-01-2019&date_to=26-05-2019&status=complete&method=open").json()

pprint(tenders)