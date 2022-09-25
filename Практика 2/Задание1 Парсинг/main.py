from bs4 import BeautifulSoup
import requests as req
import json
import tqdm

# Сюда сохраняем все спарсенные данные
data = {
    "data": []
}

# Это для обхода блокировок
sess = req.Session()
sess.headers.update({
    'location': 'https://spb.hh.ru/',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
})

# Перебираем 20 страниц по вакансии Программист Python
for page in range(0, 20):
    # По url достаем html страницы
    url = f"https://perm.hh.ru/search/vacancy?text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82" \
          f"+Python&from=suggest_post&area=1&page={page}&hhtmFrom=vacancy_search_list "
    response = sess.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    # Вычленяем по атрубуту блоки с вакансиями
    tags = soup.find_all(attrs={"data-qa": "serp-item__title"})
    for tag in tqdm.tqdm(tags):
        # Заходим внутрь каждой вакасии, чтобы достать ЗП и опыт работы
        url_obj = tag.attrs["href"]
        response_obj = sess.get(url_obj)
        soup_obj = BeautifulSoup(response_obj.text, "lxml")
        vacancy_salary = soup_obj.find(attrs={"data-qa": "vacancy-salary"})
        vacancy_experience = soup_obj.find(attrs={"data-qa": "vacancy-experience"})
        vacancy_address = soup.find(attrs={"data-qa": "vacancy-serp__vacancy-address"})
        # Складываем в data
        data["data"].append({"title":tag.text, "work experience":vacancy_experience.text, "salary":vacancy_salary.text, "region":vacancy_address.text})
        #print(tag.text, vacancy_salary.text, vacancy_experience.text, vacancy_address.text)

with open("data.json", "w") as file:
    json.dump(data, file, ensure_ascii=False)
#print(data)
