from src.db_manager import DBManager
from src.get_company_and_vacancies import get_company_data
from src.setup_database import (create_job_portal_db, insert_employer,
                                insert_vacancies)

if __name__ == "__main__":

    companies = [
        "Яндекс",
        "Mail.ru Group",
        "Сбер",
        "Ozon",
        "1С-Парус",
        "Ростех",
        "Т-Банк (Тинькофф)",
        "Wildberries",
        "PRO M8",
        "Extyl",
    ]

    def main():
        # Создание базы данных и таблиц
        create_job_portal_db()

        for company in companies:
            company_data = get_company_data(company)
            if company_data:
                employer_id = insert_employer(company_data)
                insert_vacancies(company_data["vacancies"], employer_id)
                print(f"Данные о компании '{company_data['name']}' успешно добавлены.")

        db_manager = DBManager(dbname="job_portal", user="postgres", password="123")

        companies_count = db_manager.get_companies_and_vacancies_count()
        print(companies_count)

        all_vacancies = db_manager.get_all_vacancies()
        print(all_vacancies)

        avg_salary = db_manager.get_avg_salary()
        print(avg_salary)

        high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
        print(high_salary_vacancies)

        keyword = input("Введите слово для фильтрации вакансий: ")
        keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
        print(keyword_vacancies)

        db_manager.close()

    main()
