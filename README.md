# Education App Data Model

## Project Overview
This project involves creating and simulating a data model for an education app that handles users, courses, quizzes, questions, and results. The model is designed and implemented in PostgreSQL using an ER diagram. Additionally, a Python ORM script will be used to generate realistic, normalized data for testing the model. The PostgreSQL environment is Dockerized to ensure easy setup and demonstration.

## ER Diagram

The data model is based on the following **Entity-Relationship (ER) Diagram**:

![ER Diagram](./image.png)

The diagram outlines the relationships between the major entities in the education app:

- **USER**: Represents a user in the system with attributes like `username`, `email`, `password`, and `role` (e.g., student, teacher).
- **COURSE**: Represents a course created by a user, containing quizzes.
- **QUIZ**: Represents a quiz that belongs to a course and contains multiple questions. A quiz may also be tagged with various topics.
- **QUESTION**: Represents a question within a quiz, with multiple possible answer options.
- **OPTION**: Represents the possible answers for a question, with one or more marked as correct.
- **RESPONSE**: Represents the user's submitted answers to the quiz questions.
- **RESULT**: Represents the outcome of a quiz for a user, including the total score and pass/fail status.
- **TAG**: Represents tags that categorize quizzes, allowing them to be grouped by topic.
- **QUIZ_TAG**: A junction table connecting quizzes and tags, allowing for a many-to-many relationship.

### Relationships
- A **USER** can create many **COURSES**, and each course contains multiple **QUIZZES**.
- Each **QUIZ** contains many **QUESTIONS**, and each question has multiple **OPTIONS**.
- **RESULT** tracks the scores of users who take quizzes, while **RESPONSE** records their answers to individual questions.
- **QUIZ_TAG** links quizzes with tags to categorize them into different topics.

## Getting Started

### Prerequisites
To run this project locally, you'll need the following:
- **Python** (for ORM scripting and data generation)
- **PostgreSQL** (as the database engine)
- **Docker** (for setting up a containerized environment)
- **DBeaver** or any other PostgreSQL database management tool (optional, for database visualization)

### Project Setup

1. **Clone the Repository**  
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/edu-app-data-model.git
   cd edu-app-data-model
   ```

2. **Docker Setup**  
   A `docker-compose.yml` file is included to easily set up a PostgreSQL container.

   Run the following command to start the container:
   ```bash
   docker-compose up -d
   ```

   This will create a PostgreSQL container named `education_app_db`.

3. **Environment Variables**  
   Ensure you have a `.env` file in the project root that contains the following sensitive credentials:

   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=yourpassword
   POSTGRES_DB=postgres
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```


4. **Create Physical Tables**  
   Once the PostgreSQL container is running, the physical tables can be created using the SQL file `tables.sql`.  
   You can run the SQL commands inside DBeaver or any PostgreSQL client:

   ```sql
   \i sql/tables.sql
   ```

   This will create all the necessary tables, including **USERS**, **COURSE**, **QUIZ**, **QUESTION**, **OPTION**, **RESULT**, **RESPONSE**, **TAG**, and **QUIZ_TAG**.


5. **.gitignore**  
   The `.gitignore` file includes rules to ignore sensitive files like `.env`, Python cache files, and Docker data:
