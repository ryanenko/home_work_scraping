import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import re

pattern = r"(\w+\d+)*[\u202f]*(\d+)*"
pattern_sub = r"\1\2"
Host = 'https://spb.hh.ru/search/vacancy'
params = {'text' : 'python django flask', 'from' : 'suggest_post', 'salary': '', 'area': [1, 2], 'ored_clusters' : 'true', 'enable_snippets' : 'true'}

def get_headers():
    headers = Headers(browser='firefox', os='win').generate()
    return headers

hh_html = requests.get(Host, params=params, headers=get_headers()).text

soup = BeautifulSoup(hh_html, features='lxml')
list_tag = soup.find(class_="vacancy-serp-content")

job_list = []
list_title = list_tag.find_all('div', class_= 'vacancy-serp-item-body__main-info')

for i in list_title:
    title=i.find('a',class_="serp-item__title" ).text
    link = i.find('a',class_="serp-item__title" )['href']
    city = i.find('div',{"data-qa": "vacancy-serp__vacancy-address"}).text
    salary_link = i.find('span', class_= 'bloko-header-section-3')
    pprint(salary_link)
    if salary_link == None:
        salary = 'Не указан'
    else:
        salary = re.sub(pattern, pattern_sub, salary_link.text )   
    job_list.append({'title':title, 'link': link, 'city':city, 'salary': salary})




with open ('job_list.json', 'w', encoding='utf-8') as fp:
    json.dump(job_list, fp, ensure_ascii=False, indent=2)






   
     
   




