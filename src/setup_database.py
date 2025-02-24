import psycopg2


def create_job_portal_db():
    """Создает БД 'job_portal' и таблицы в ней"""

    # Параметры подключения к базе данных postgres
    db_params = {
        "database": "postgres",
        "user": "postgres",
        "password": "123",
        "host": "localhost",
        "port": "5432",
    }

    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    conn.autocommit = True
    cursor = conn.cursor()

    # Создание базы данных job_portal
    cursor.execute("CREATE DATABASE job_portal;")
    cursor.close()
    conn.close()

    # Параметры подключения к новой базе данных
    db_params["database"] = "job_portal"

    # Подключение к новой базе данных
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Создание таблицы employers
    cursor.execute(
        """
        CREATE TABLE employers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            url VARCHAR(255),
            vacancies_count INTEGER DEFAULT 0
        );
    """
    )

    # Создание таблицы vacancies
    cursor.execute(
        """
        CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            url VARCHAR(255),
            salary_from DECIMAL,
            salary_to DECIMAL,
            currency VARCHAR(10),
            employer_id INTEGER REFERENCES employers(id)
        );
    """
    )

    # Закрытие соединения
    cursor.close()
    conn.commit()
    conn.close()


def insert_employer(data):
    """Добавляет работодателя в таблицу employers."""
    conn = psycopg2.connect(
        dbname="job_portal", user="postgres", password="123", host="localhost"
    )
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO employers (name, url, vacancies_count)
        VALUES (%s, %s, %s) RETURNING id;
    """,
        (data["name"], data["url"], data["vacancies_count"]),
    )

    employer_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return employer_id


def insert_vacancies(vacancies, employer_id):
    """Добавляет вакансии в таблицу vacancies."""
    conn = psycopg2.connect(
        dbname="job_portal", user="postgres", password="123", host="localhost"
    )
    cursor = conn.cursor()

    for vacancy in vacancies:
        if vacancy is None:
            continue

        salary_from = vacancy.get("salary", {}).get("from")
        salary_to = vacancy.get("salary", {}).get("to")
        currency = vacancy.get("salary", {}).get("currency", "RUB")

        cursor.execute(
            """
            INSERT INTO vacancies (title, url, salary_from, salary_to, currency, employer_id)
            VALUES (%s, %s, %s, %s, %s, %s);
        """,
            (
                vacancy.get("title"),
                vacancy.get("url"),
                salary_from,
                salary_to,
                currency,
                employer_id,
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()
