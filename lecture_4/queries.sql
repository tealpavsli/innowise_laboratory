-- 1. Найти все оценки для конкретного студента (Alice Johnson)
SELECT g.* 
FROM grades g
JOIN students s ON g.student_id = s.id
WHERE s.full_name = 'Alice Johnson';

-- 2. Рассчитать средний балл по каждому студенту
SELECT s.id, s.full_name,
       ROUND(AVG(g.grade), 2) AS avg_grade,
       COUNT(g.grade) AS grades_count
FROM students s
LEFT JOIN grades g ON g.student_id = s.id
GROUP BY s.id, s.full_name
ORDER BY avg_grade DESC;

-- 3. Список всех студентов, рождённых после 2004
SELECT * FROM students WHERE birth_year > 2004 ORDER BY birth_year;

-- 4. Запрос, который перечисляет все предметы и их средние оценки
SELECT subject, ROUND(AVG(grade), 2) AS avg_grade, COUNT(*) AS cnt
FROM grades
GROUP BY subject
ORDER BY avg_grade DESC;

-- 5. Топ-3 студента с наивысшим средним баллом
SELECT s.full_name, ROUND(AVG(g.grade), 2) AS avg_grade
FROM students s
JOIN grades g ON g.student_id = s.id
GROUP BY s.id
HAVING COUNT(g.grade) > 0
ORDER BY avg_grade DESC
LIMIT 3;

-- 6. Показать всех студентов, у которых есть хотя бы одна оценка ниже 80
SELECT DISTINCT s.full_name
FROM students s
JOIN grades g ON g.student_id = s.id
WHERE g.grade < 80
ORDER BY s.full_name;
