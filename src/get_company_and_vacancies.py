import requests


def get_company_data(company_name):
    """Получает данные о компании и её вакансиях по имени."""
    url = "https://api.hh.ru/employers"
    params = {"text": company_name}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["found"] > 0:
            employer = data["items"][0]
            employer_id = employer["id"]
            employer_name = employer["name"]
            employer_url = employer["alternate_url"]

            vacancies_data = get_vacancies_by_company(employer_id)
            return {
                "name": employer_name,
                "url": employer_url,
                "vacancies_count": len(vacancies_data),
                "vacancies": vacancies_data,
            }
        else:
            print(f"Компания '{company_name}' не найдена.")
            return None
    else:
        print(
            f"Ошибка при получении данных для компании '{company_name}': {response.status_code}"
        )
        return None


def get_vacancies_by_company(company_id):
    """Получает вакансии для компании по её ID."""
    url = "https://api.hh.ru/vacancies"
    params = {"employer_id": company_id, "per_page": 100}
    vacancies = []

    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            vacancies.extend(data["items"])
            if data["pages"] > data["page"]:
                params["page"] = data["page"] + 1
            else:
                break
        else:
            print(f"Ошибка при получении вакансий: {response.status_code}")
            break

    return [
        {
            "title": vacancy["name"],
            "url": vacancy["alternate_url"],
            "salary": vacancy.get("salary", {}),
        }
        for vacancy in vacancies
    ]
