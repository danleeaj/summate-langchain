import sqlite3
import uuid
from typing import Tuple, List
import os

class DatabaseManager:
    def __init__(self, database_name: str = "database.db"):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        db_dir = os.path.join(app_dir, "db")
        os.makedirs(db_dir, exist_ok=True)

        self.db_path = os.path.join(db_dir, database_name)

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_tables() # Creates all tables that do not exist yet

    def _create_tables(self):
        """Create all tables if they don't exist."""
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS QUESTION (
                                  id TEXT PRIMARY KEY,
                                  question TEXT NOT NULL
                                  );
            CREATE TABLE IF NOT EXISTS RUBRIC (
                                  id TEXT PRIMARY KEY,
                                  component TEXT NOT NULL,
                                  question_id TEXT,
                                  rubric_index INTEGER,
                                  FOREIGN KEY (question_id) REFERENCES QUESTION(id)
                                  );
            CREATE TABLE IF NOT EXISTS RESPONSE (
                                  id TEXT PRIMARY KEY,
                                  response TEXT NOT NULL,
                                  question_id TEXT,
                                  FOREIGN KEY (question_id) REFERENCES QUESTION(id)
                                  );
            CREATE TABLE IF NOT EXISTS EVALUATION (
                                  id TEXT PRIMARY KEY,
                                  evaluation BOOLEAN NOT NULL,
                                  debug_path TEXT NOT NULL,
                                  rubric_id TEXT,
                                  response_id TEXT,
                                  FOREIGN KEY (rubric_id) REFERENCES RUBRIC(id),
                                  FOREIGN KEY (response_id) REFERENCES RESPONSE(id)
                                  );
        """)
        self.conn.commit()

    def add_question(self, question:str) -> str:
        """Adds question. Returns: ID (str)"""
        question_id = str(uuid.uuid4())
        self.cursor.execute(
            "INSERT INTO QUESTION (ID, question) VALUES (?, ?)",
            (question_id, question)
        )
        self.conn.commit()
        return question_id
    
    def add_rubric(self, component: str, question_id: str, rubric_index: int) -> str:
        """Adds rubric component. The question ID must be specified. The rubric index is an int used for ordering rubric when returned to the user. Returns: ID (str)"""
        rubric_id = str(uuid.uuid4())
        self.cursor.execute(
            "INSERT INTO RUBRIC (ID, component, question_id, rubric_index) VALUES (?, ?, ?, ?)",
            (rubric_id, component, question_id, rubric_index)
        )
        self.conn.commit()
        return rubric_id

    def add_response(self, response: str, question_id: str) -> str:
        """Adds response. The question ID must be specified. Returns: ID (str)"""
        response_id = str(uuid.uuid4())
        self.cursor.execute(
            "INSERT INTO RESPONSE (ID, response, question_ID) VALUES (?, ?, ?)",
            (response_id, response, question_id)
        )
        self.conn.commit()
        return response_id

    def add_evaluation(self, evaluation: bool, debug_path: str, rubric_id: str, response_id: str) -> str:
        """Adds evaluation. The rubric and response ID must be specified. Returns: ID"""
        evaluation_id = str(uuid.uuid4())
        self.cursor.execute(
            """INSERT INTO EVALUATION 
               (id, evaluation, debug_path, rubric_id, response_id) 
               VALUES (?, ?, ?, ?, ?)""",
            (evaluation_id, evaluation, debug_path, rubric_id, response_id)
        )
        self.conn.commit()
        return evaluation_id
    
    def delete_question(self, question_id: str):
        """Delete a question and all related entries."""
        self.cursor.execute("DELETE FROM QUESTION WHERE id = ?", (question_id,))
        self.cursor.execute("DELETE FROM RUBRIC WHERE question_id = ?", (question_id,))
        self.cursor.execute("DELETE FROM RESPONSE WHERE question_id = ?", (question_id,))
        self.conn.commit()
    
    def delete_rubric(self, rubric_id: str):
        """Delete a rubric."""
        self.cursor.execute("DELETE FROM RUBRIC WHERE rubric_id = ?", (rubric_id,))
        self.conn.commit()

    def delete_response(self, response_id: str):
        """Delete a response."""
        self.cursor.execute("DELETE FROM RESPONSE WHERE rubric_id = ?", (response_id,))
        self.conn.commit()

    def get_evaluations_for_response(self, response_id: str) -> List[Tuple]:
        """Get all evaluations for a specific response."""
        self.cursor.execute(
            """SELECT ID, evaluation, debug_path, rubric_id, response_id FROM EVALUATION WHERE response_id = ?""",
            (response_id,)
        )
        return self.cursor.fetchall()

    def close(self):
        """Close database connection."""
        self.conn.close()

    # These allow the class to be used with the with statement.

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()