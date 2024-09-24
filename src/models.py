from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Boolean, TIMESTAMP, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Set up connection string for PostgreSQL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Base for SQLAlchemy ORM models
Base = declarative_base()

# Define models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)

    # Relationships
    created_courses = relationship("Course", back_populates="creator", cascade="all, delete-orphan")
    created_quizzes = relationship("Quiz", back_populates="creator", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="user", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="user", cascade="all, delete-orphan")


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    course_name = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    creator = relationship("User", back_populates="created_courses")
    quizzes = relationship("Quiz", back_populates="course", cascade="all, delete-orphan")


class Quiz(Base):
    __tablename__ = 'quizzes'
    id = Column(Integer, primary_key=True)
    quiz_name = Column(String(255), nullable=False)
    description = Column(Text)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'))
    created_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)

    # Relationships
    course = relationship("Course", back_populates="quizzes")
    creator = relationship("User", back_populates="created_quizzes")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="quiz_tags", back_populates="quizzes")
    results = relationship("Result", back_populates="quiz", cascade="all, delete-orphan")


# Many-to-Many relationship between Quiz and Tag
quiz_tag = Table('quiz_tags', Base.metadata,
    Column('quiz_id', Integer, ForeignKey('quizzes.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    # Relationships
    quizzes = relationship("Quiz", secondary=quiz_tag, back_populates="tags")


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quizzes.id', ondelete='CASCADE'))

    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")


class Option(Base):
    __tablename__ = 'options'
    id = Column(Integer, primary_key=True)
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'))

    # Relationships
    question = relationship("Question", back_populates="options")


class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    quiz_id = Column(Integer, ForeignKey('quizzes.id', ondelete='CASCADE'))
    total_score = Column(Integer)
    passed = Column(Boolean, nullable=False)

    # Relationships
    user = relationship("User", back_populates="results")
    quiz = relationship("Quiz", back_populates="results")


class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'))
    option_id = Column(Integer, ForeignKey('options.id', ondelete='SET NULL'))
    submitted_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="responses")
    question = relationship("Question")
    option = relationship("Option")


# Create an engine to connect to PostgreSQL
engine = create_engine('postgresql://postgres:POSTGRESmalsha%403@localhost:5432/postgres')


# Create all tables in the database
Base.metadata.create_all(engine)
