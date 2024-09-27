--To check if every quiz has at least one question
SELECT q.quiz_name, COUNT(qu.id) as num_questions2
FROM quizzes q
LEFT JOIN questions qu ON q.id = qu.quiz_id
GROUP BY q.quiz_name
HAVING COUNT(qu.id) = 0;

--To check every quiz has been taken by atleast one user (based on the results table)
SELECT q.quiz_name, COUNT(r.id) as num_results
FROM quizzes q
LEFT JOIN results r ON q.id = r.quiz_id
GROUP BY q.quiz_name
HAVING COUNT(r.id) = 0;

--To Identify users who haven’t attempted any quizzes
SELECT u.username, COUNT(r.id) as num_attempts
FROM users u
LEFT JOIN results r ON u.id = r.user_id
GROUP BY u.username
HAVING COUNT(r.id) = 0;

--To check the questions with no options
SELECT q.question_text, COUNT(o.id) as num_options
FROM questions q
LEFT JOIN options o ON q.id = o.question_id
GROUP BY q.question_text
HAVING COUNT(o.id) = 0;

--To check if each course has quizzes
SELECT c.course_name, COUNT(q.id) as num_quizzes
FROM courses c
LEFT JOIN quizzes q ON c.id = q.course_id
GROUP BY c.course_name
HAVING COUNT(q.id) = 0;

--To check the average score for quizzes and analyze pass rates
SELECT quiz_id, 
       AVG(total_score) as avg_score, 
       SUM(passed::int) as num_passed, 
       COUNT(*) as total_attempts
FROM results
GROUP BY quiz_id;

--To Identify quizzes that don't have tags
SELECT q.quiz_name, COUNT(qt.tag_id) as num_tags
FROM quizzes q
LEFT JOIN quiz_tags qt ON q.id = qt.quiz_id
GROUP BY q.quiz_name
HAVING COUNT(qt.tag_id) = 0;


