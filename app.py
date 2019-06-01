# coding=utf-8
# macos: python3 app.py

import requests
import time
import pandas as pd
import itertools
from pprint import pprint
import statistics

print('app is started')

#1. API Prozorro.gov.ua
# Посилання: https://prozorro.gov.ua/
# Документація: https://prozorro.gov.ua/openprocurement
# Модуль аналітики: https://bi.prozorro.org/

# Завдання #1: ознайомитись з даними Prozorro
# отримаємо перелік тендерів з системи
# tender_list = requests.get("https://public.api.openprocurement.org/api/2.5/tenders").json()
# pprint(tender_list)

# отримаємо тендер за ідентифікатором
# переглянути тендер у веб: https://prozorro.gov.ua/tender/UA-2019-05-28-001297-a
# tender = requests.get("https://public.api.openprocurement.org/api/2.5/tenders/41a2ea0d76604c7198a333fc382f30e6").json()
# pprint(tender)

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

# tenders = requests.get("https://clarity-project.info/api/tender.search?entity=03365245&date_from=01-01-2019&date_to=26-05-2019&status=complete&method=open").json()

# pprint(tenders)

# tender_id = []
# tender_amount = []
# tender_title = []
# tender_risk = []
#
# for t in tenders["tenders"]:

    # у ризиках є незаповнені значення, тому напишемо умову
    # if t["risks"]["score"] != None:
    #     # розрахуємо ризик у %
    #     risk_score = int(t["risks"]["score"])
    #     risk_max = int(t["risks"]["max"])
    #     score_in_percent = (risk_score / risk_max) * 100
    #     tender_risk.append(score_in_percent)
    #
    #     # назви та ідентифікатори тендерів
    #     tender_id.append(t["id"])
    #     tender_title.append(t["title"])
    #     tender_amount.append(float(t["value"]["amount"]))

# створимо таблицю
# tenders_df = pd.DataFrame({"tender_id": tender_id,
#                            "tender_amount": tender_amount,
#                            "tender_title": tender_title,
#                            "tender_risk": tender_risk}).sort_values(by="tender_risk", ascending=False)
#
# tenders_df

# побудуємо графік розсіювання (scatter plot) вартості закупівлі проти ризику
# tenders_df.plot.scatter(x='tender_amount', y='tender_risk')

# перевіримо три набільш ризикованих тендери на Dozorro
# для цього необіхдно перевести
# for i in tenders_df.iloc[0:3, 0]:
#   id = requests.get("https://clarity-project.info/api/tender.ids?ids=" + i).json()
#   id = id["list"][0]["tender"]
#   print("https://dozorro.org/tender/" + id)
#   time.sleep(0.25)


# API Єдного державного веб-порталу публічних фінансів (spending.gov.ua)
# Посилання: https://spending.gov.ua/
# Документація: https://confluence.spending.gov.ua/display/ds/API?src=contextnavpagetreemode
# Севіс для зручного пошуку: https://www.007.org.ua/
#
# Нормативка:
# 1. Закон України "Про відкритість використання публічних коштів"
#
# Завдання #3. Знайти установу, яка провела найбільше відряджень
# (1) Створимо переілк розпорядників
# ids = ["03365245", "23227605", "02228823", "26321546", "04055251", "05403286", "34629018", "02498694", "41844557",
#        "30386669", "37623993", "02314122", "22218863", "26449743", "25966502", "42215510", "13768872", "37624028",
#        "36200391", "41844390", "42188147", "42652979"]

# (2) Отримаємо звіти розпорядників. Через точку доступу: http://api.spending.gov.ua/api/v2/api/reports/{}/page?reportTypeId=3&reportTypeId=43
# list_of_reports = []
#
# for i in ids:
#     url = "http://api.spending.gov.ua/api/v2/api/reports/{}/page?reportTypeId=3&reportTypeId=43".format(i)
#     response = requests.get(url).json()["content"]
#     list_of_reports.append(response)
#     time.sleep(0.25)
#
# len(list_of_reports)

# (3) Ми отримали масив масиів: [[1, 2],[3, 4],[5, 6]]. Для подальшої роботи його треба зробити плоским: [1, 2, 3, 4, 5, 6].
# [[1, 2],[3, 4],[5, 6]] -> [1, 2, 3, 4, 5, 6]

# reports = []
#
# for page in list_of_reports:
#   for r in page:
#     reports.append(r)

# зробити теж саме через готову функцію
# reports = list(itertools.chain(*list_of_reports))

# len(list_of_reports)
# len(reports)

# (4) З кожного звіту витягнемо необхідні поля
# reportId = []
# reportEDR = []
# publishDate = []
#
# for i in reports:
#   reportId.append(i['reportId'])
#   reportEDR.append(i['edrpou'] )
#   publishDate.append(i['publishDate'])

# (5) А дані про суми відряджень, ми отрмуємо з іншої точки доступу: http://api.spending.gov.ua/api/v2/api/reports/
# report_amount = []

# треба зробити цикл для двох масивів паралельно
# for r, i  in zip(reportId, reportEDR):
#   url = "http://api.spending.gov.ua/api/v2/api/reports/{}/{}".format(i, r)
#   response = requests.get(url).json()["data"][1]["cells"][0]
#   report_amount.append(response)
#   time.sleep(0)

# (6) Створимо табличку
# reports_df = pd.DataFrame({"reportId": reportId,
#                            "reportEDR": reportEDR,
#                            "publishDate": publishDate,
#                            "report_amount": report_amount}, index = publishDate)

# перетворюємо поля таблиць у формати дат та чисел
# reports_df["report_amount"] = pd.to_numeric(reports_df["report_amount"])
# reports_df["publishDate"] = to_datetime(reports_df["publishDate"])
#
# reports_df.groupby("reportEDR").sum()




# API Єдиного державного веб порталу відкритих даних (data.gov.ua)
# Посилання: https://data.gov.ua/
# Документація: https://docs.ckan.org/en/2.8/api/
# Суперсила: отримувати дані з таблиць через SQL запити.
#
# API до метаданих
# API до файлів
# API до сховища диних
# Приклад. Ваканції державної служби зайнятості

# запит в ідеальному світі: SELECT * from "resource-id" WHERE columnTitle='some_string'

# запит для Держслужбизайтятості
query = "SELECT * from \"a9dafeab-620c-4907-8b8b-5cf3798122d7\" WHERE \"ЦЗ реєстрації (назва) / Оперативн\"='КІРОВОГРАДСЬКИЙ МІСЬКРАЙОННИЙ ЦЕНТР ЗАЙНЯТОСТІ'"

vacancies = requests.get("https://data.gov.ua/api/3/action/datastore_search_sql?sql=" + query).json()

# подивимось розподіл заробітних плат
salaries = []
for i in vacancies['result']['records']:
  salaries.append(
      float(i['Заробітна плата / Оперативні вака'])
  )


# pd.Series(salaries).hist(bins=10)
# print("Медіана ЗП: " + str(statistics.median(salaries)))
# print("Середня ЗП: " + str(statistics.mean(salaries)))



# Моєму проекту потрібні відкриті реєстри. Які є опції?
# Довгий шлях: скачувати дані з порталу, чистити, формувати власні бази даних.
# Короткий шлях: підключитися до одного з існуючих API.
#
# Відкриті API (безкоштовні)
# Ring API
# Clarity Project API
# Суд на долоні API (частково безкоштовний)

# Платні API
# OpenDataBot API

# Що цікаве подивитись на порталі?
# Міністерство внутрішніх справ України
# Державна фіскальна служба
# Центральна виборча комісія
# Національний банк Украйни
# Міністерство юстиції України
# Державна судова адміністрація України
# Міністерство інфраструктури України

# Не на порталі:
# Портал відкритих даних даних Верховної Ради України
# Відкриті дані Міністерства освіти України
# Національна служба здоров'я України

# Неформальні спільноти
# OpenDataBot: все про відкриті дані: Facebook. Telegram.
# OpenUP: Facebook.
# OpenData835: Facebook, Telegram




# API Інспекційного порталу (inspections.gov.ua)
# Посилання: https://inspections.gov.ua/
# Документація: http://api.ias.brdo.com.ua/v1_1/manual
# Модуль аналітики: https://inspections.gov.ua/regulator/analytics
# Важливо: API закрите. Щоб отримати ключ, зверніться за адресою ias@brdo.com.ua.
#
# Нормативна база:
#
# Закон України "Про основні засади державного нагляду (контролю) у сфері господарської діяльності"
# Галузева нормативка
# Завдання #3: Ознайомитись з іnspections.gov.ua
# отримати перелік всіх інспектувань в системі
# inspections = requests.get("http://api.ias.brdo.com.ua/v1_1/inspections?apiKey=brdo-key-4512896734821100").json()
# pprint(inspections)

# отримати інспекцію за ідентифікатором
# inspection = requests.get("http://api.ias.brdo.com.ua/v1_1/inspection?apiKey=brdo-key-4512896734821100&inspectionId=fffefeac52b12730c13fcd76a248f711647c2e7f").json()
# pprint(inspections)


# Завдання #4: Ознайомитись з іnspections.gov.ua
# запит
# key = brdo-key-4512896734821100 | мій ключ (прохання не викорстовувати для великих проектів)
# from = 01-01-2018 & to = 01-06-2018 | часовий інтервал
# regulator = Управління ДСНС у Кіровоградській області | орган, що здійснює інспектування
# current-page = 1 | сторінка

insp_pages = []

# for i in range(1, 3):
for i in range(1, 2):
    url = "http://api.ias.brdo.com.ua/v1_1/inspections?apiKey=brdo-key-4512896734821100&from=01-05-2019&to=01-06-2019&regulator=Управління ДСНС у Кіровоградській області&current-page={}".format(
        i)
    json = requests.get(url).json()["items"]
    insp_pages.append(json)
    time.sleep(0.25)

# робимо масив плоским [[1, 2],[3, 4],[5, 6]] -> [1, 2, 3, 4, 5, 6]
inspections = []
for page in insp_pages:
    for i in page:
        inspections.append(i)

# короткий шлях зробити масив плоским: inspections = list(itertools.chain(*insp_pages)))

violations_number = []
address = []
name = []

for i in inspections:
    # беремо лише ті де є порушення
    if (i["data"]["violations"] != False and i["data"]["risk"] == "Високий"):
        violations_number.append(len(i["data"]["violations"]))
        address.append(i["data"]["address"])
        name.append(i["data"]["name"])

inspections_df = pd.DataFrame({"name": name,
                               "address": address,
                               "violations_number": violations_number}).sort_values(by="violations_number",
                                                                                    ascending=False)
# inspections_df
pprint(inspections)