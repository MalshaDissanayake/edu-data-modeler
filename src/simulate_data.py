from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import User, Course, Quiz, Question, Option, Tag, quiz_tag, Result, Response, engine
from sqlalchemy import insert

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()

# Initialize Faker
fake = Faker()

# Seed Users
def seed_users(num_users=10):
    users = []
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
            role=fake.random_element(elements=('student', 'teacher'))
        )
        users.append(user)
        session.add(user)
    session.commit()
    return users

# Seed Courses
def seed_courses(users, num_courses=5):
    courses = []
    for _ in range(num_courses):
        course = Course(
            course_name=fake.catch_phrase(),
            description=fake.text(),
            created_by=fake.random_element(users).id
        )
        courses.append(course)
        session.add(course)
    session.commit()
    return courses

# Seed Quizzes
def seed_quizzes(courses, users, num_quizzes=5):
    quizzes = []
    for _ in range(num_quizzes):
        quiz = Quiz(
            quiz_name=fake.catch_phrase(),
            description=fake.text(),
            course_id=fake.random_element(courses).id,
            created_by=fake.random_element(users).id,
            start_time=fake.date_time_this_year(),
            end_time=fake.date_time_this_year()
        )
        quizzes.append(quiz)
        session.add(quiz)
    session.commit()
    return quizzes

# Seed Tags
def seed_tags(num_tags=5):
    tags = []
    for _ in range(num_tags):
        tag = Tag(
            name=fake.word()
        )
        tags.append(tag)
        session.add(tag)
    session.commit()
    return tags

# Seed Quiz Tags (Many-to-Many)
def seed_quiz_tags(quizzes, tags):
    for quiz in quizzes:
        for _ in range(fake.random_int(min=1, max=3)):
            stmt = insert(quiz_tag).values(
                quiz_id=quiz.id,
                tag_id=fake.random_element(tags).id
            )
            session.execute(stmt)
    session.commit()

# Seed Questions
def seed_questions(quizzes, num_questions=5):
    questions = []
    for quiz in quizzes:
        for _ in range(num_questions):
            question = Question(
                question_text=fake.sentence(),
                question_type=fake.random_element(elements=('multiple_choice', 'true_false')),
                quiz_id=quiz.id
            )
            questions.append(question)
            session.add(question)
    session.commit()
    return questions

# Seed Options for Questions
def seed_options(questions):
    options = []
    for question in questions:
        for _ in range(4):  # Assuming 4 options per question
            option = Option(
                option_text=fake.sentence(),
                is_correct=fake.boolean(),
                question_id=question.id
            )
            options.append(option)
            session.add(option)
    session.commit()

# Seed Results
def seed_results(users, quizzes):
    results = []
    for user in users:
        for quiz in quizzes:
            result = Result(
                user_id=user.id,
                quiz_id=quiz.id,
                total_score=fake.random_int(min=0, max=100),
                passed=fake.boolean()
            )
            results.append(result)
            session.add(result)
    session.commit()

# Seed Responses
def seed_responses(users, questions, options):
    for user in users:
        for question in questions:
            response = Response(
                user_id=user.id,
                question_id=question.id,
                option_id=fake.random_element(options).id,
                submitted_at=fake.date_time_this_year()
            )
            session.add(response)
    session.commit()

# Main Seeding Function
def main_seeding():
    # Step 1: Seed Users
    users = seed_users()

    # Step 2: Seed Courses
    courses = seed_courses(users)

    # Step 3: Seed Quizzes
    quizzes = seed_quizzes(courses, users)

    # Step 4: Seed Tags
    tags = seed_tags()

    # Step 5: Seed Quiz Tags (Many-to-Many relation between Quizzes and Tags)
    seed_quiz_tags(quizzes, tags)

    # Step 6: Seed Questions for Quizzes
    questions = seed_questions(quizzes)

    # Step 7: Seed Options for Questions
    seed_options(questions)

    # Step 8: Seed Results for Users' Quiz attempts
    seed_results(users, quizzes)

    # Step 9: Seed Responses (Users' answers to quiz questions)
    seed_responses(users, questions, session.query(Option).all())

    print("Seeding completed successfully!")

# Run the main seeding function
if __name__ == "__main__":
    main_seeding()

# Close the session after seeding
session.close()