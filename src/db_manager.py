import psycopg2


class DBManager:
    def __init__(self, dbname, user, password, host="localhost"):
        """Конструктор класса, который устанавливает соединение с базой данных PostgreSQL."""
        self.connection = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host
        )
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        query = """
        SELECT employers.name, COUNT(vacancies.id)         
        FROM employers 
        LEFT JOIN vacancies ON employers.id = vacancies.employer_id 
        GROUP BY employers.name;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        output = "Компании и количество вакансий:\n"
        for company, count in results:
            output += f"{company}: {count} вакансий\n"
        return output.strip()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию."""
        query = """
        SELECT employers.name, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.url 
        FROM vacancies 
        JOIN employers ON vacancies.employer_id = employers.id;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        output = "Все вакансии:\n"
        for employer_name, title, salary_from, salary_to, url in results:
            output += (
                f"{title} в компании {employer_name}: Зарплата от {salary_from} до {salary_to} - "
                f"[Ссылка]({url})\n"
            )
        return output.strip()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        query = """
        SELECT AVG(salary_from) 
        FROM vacancies;
        """
        self.cursor.execute(query)
        avg_salary = self.cursor.fetchone()[0]
        return f"Средняя зарплата по вакансиям: {round(avg_salary, 2)}"

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = float(self.get_avg_salary().split(": ")[1])
        query = """
        SELECT employers.name, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.url 
        FROM vacancies 
        JOIN employers ON vacancies.employer_id = employers.id 
        WHERE salary_from > %s;
        """
        self.cursor.execute(query, (avg_salary,))
        results = self.cursor.fetchall()

        output = f"Вакансии с зарплатой выше {round(avg_salary, 2)}:\n"
        for employer_name, title, salary_from, salary_to, url in results:
            output += (
                f"{title} в компании {employer_name}: Зарплата от {salary_from} до {salary_to} - "
                f"[Ссылка]({url})\n"
            )
        return output.strip()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        query = """
        SELECT employers.name, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.url 
        FROM vacancies 
        JOIN employers ON vacancies.employer_id = employers.id 
        WHERE vacancies.title ILIKE %s;
        """
        self.cursor.execute(query, (f"%{keyword}%",))
        results = self.cursor.fetchall()

        output = f"Вакансии, содержащие слово '{keyword}':\n"
        for employer_name, title, salary_from, salary_to, url in results:
            output += (
                f"{title} в компании {employer_name}: Зарплата от {salary_from} до {salary_to} - "
                f"[Ссылка]({url})\n"
            )
        return output.strip()

    def close(self):
        """Закрывает курсор и соединение с базой данных."""
        self.cursor.close()
        self.connection.close()
