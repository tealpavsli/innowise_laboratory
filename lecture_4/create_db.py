"""
create_db.py
Создаёт SQLite базу school.db и заполняет таблицы students и grades.
Запуск: python lecture_4\create_db.py
"""
from typing import List, Tuple
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "school.db"


def create_tables(conn: sqlite3.Connection) -> None:
    """Создать таблицы students и grades."""
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            birth_year INTEGER NOT NULL
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            grade INTEGER NOT NULL CHECK(grade BETWEEN 0 AND 100),
            FOREIGN KEY (student_id) REFERENCES students(id)
        );
        """
    )
    conn.commit()


def insert_sample_data(conn: sqlite3.Connection) -> None:
    """Вставить примеры данных (students + grades)."""
    cur = conn.cursor()

    students: List[Tuple[str, int]] = [
        ("Alice Johnson", 2005),
        ("Brian Smith", 2004),
        ("Carla Reyes", 2006),
        ("Daniel Kim", 2005),
        ("Eva Thompson", 2003),
        ("Felix Nguyen", 2007),
        ("Grace Patel", 2005),
        ("Henry Lopez", 2004),
        ("Isabella Martinez", 2006),
    ]

    # Вставка студентов (очищаем дубликаты при повторном запуске)
    cur.execute("DELETE FROM grades;")
    cur.execute("DELETE FROM students;")
    conn.commit()

    cur.executemany("INSERT INTO students (full_name, birth_year) VALUES (?, ?);", students)
    conn.commit()

    # Получаем id студентов (в порядке вставки)
    cur.execute("SELECT id, full_name FROM students ORDER BY id;")
    rows = cur.fetchall()
    id_map = {row[1]: row[0] for row in rows}

    # Данные оценок — используйте id_map для подстановки student_id
    grades = [
        (id_map["Alice Johnson"], "Math", 88),
        (id_map["Alice Johnson"], "English", 92),
        (id_map["Alice Johnson"], "Science", 85),

        (id_map["Brian Smith"], "Math", 75),
        (id_map["Brian Smith"], "History", 83),
        (id_map["Brian Smith"], "English", 79),

        (id_map["Carla Reyes"], "Science", 95),
        (id_map["Carla Reyes"], "Math", 91),
        (id_map["Carla Reyes"], "Art", 89),

        (id_map["Daniel Kim"], "Math", 84),
        (id_map["Daniel Kim"], "Science", 88),
        (id_map["Daniel Kim"], "Physical Education", 93),

        (id_map["Eva Thompson"], "English", 90),
        (id_map["Eva Thompson"], "History", 85),
        (id_map["Eva Thompson"], "Math", 88),

        (id_map["Felix Nguyen"], "Science", 72),
        (id_map["Felix Nguyen"], "Math", 78),
        (id_map["Felix Nguyen"], "English", 81),

        (id_map["Grace Patel"], "Art", 94),
        (id_map["Grace Patel"], "Science", 87),
        (id_map["Grace Patel"], "Math", 90),

        (id_map["Henry Lopez"], "History", 77),
        (id_map["Henry Lopez"], "Math", 83),
        (id_map["Henry Lopez"], "Science", 80),

        (id_map["Isabella Martinez"], "English", 96),
        (id_map["Isabella Martinez"], "Math", 89),
        (id_map["Isabella Martinez"], "Art", 92),
    ]

    cur.executemany("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?);", grades)
    conn.commit()


def create_indexes(conn: sqlite3.Connection) -> None:
    """Опционально: создать индексы для ускорения запросов."""
    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_grades_student ON grades(student_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject);")
    conn.commit()


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH.as_posix())
    try:
        create_tables(conn)
        insert_sample_data(conn)
        create_indexes(conn)
        print(f"Database created and populated at: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
