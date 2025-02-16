import pytest
import os
from app.utils.database_manager import DatabaseManager
import sqlite3

@pytest.fixture
def db_manager():
    """Fixture to create a test database instance"""
    # Use an in-memory database for testing
    db = DatabaseManager("test_database.db")
    yield db
    
    # Cleanup after tests
    db.close()
    if os.path.exists(db.db_path):
        os.remove(db.db_path)

def test_database_initialization(db_manager):
    """Test that database is properly initialized with required tables"""
    cursor = db_manager.cursor
    
    # Check if all tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    
    expected_tables = {'QUESTION', 'RUBRIC', 'RESPONSE', 'EVALUATION'}
    assert expected_tables.issubset(tables)

def test_add_question(db_manager):
    """Test adding a question"""
    question = "What is the capital of France?"
    question_id = db_manager.add_question(question)
    
    # Verify question was added
    cursor = db_manager.cursor
    cursor.execute("SELECT question FROM QUESTION WHERE id = ?", (question_id,))
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == question

def test_add_rubric(db_manager):
    """Test adding a rubric component"""
    # First add a question
    question_id = db_manager.add_question("Test question")
    
    # Add rubric
    component = "Must mention Paris"
    rubric_index = 1
    rubric_id = db_manager.add_rubric(component, question_id, rubric_index)
    
    # Verify rubric was added
    cursor = db_manager.cursor
    cursor.execute("SELECT component, question_id, rubric_index FROM RUBRIC WHERE id = ?", (rubric_id,))
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == component
    assert result[1] == question_id
    assert result[2] == rubric_index

def test_add_response(db_manager):
    """Test adding a response"""
    # First add a question
    question_id = db_manager.add_question("Test question")
    
    # Add response
    response = "Paris is the capital of France"
    response_id = db_manager.add_response(response, question_id)
    
    # Verify response was added
    cursor = db_manager.cursor
    cursor.execute("SELECT response, question_id FROM RESPONSE WHERE id = ?", (response_id,))
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == response
    assert result[1] == question_id

def test_add_evaluation(db_manager):
    """Test adding an evaluation"""
    # Setup required foreign keys
    question_id = db_manager.add_question("Test question")
    rubric_id = db_manager.add_rubric("Test rubric", question_id, 1)
    response_id = db_manager.add_response("Test response", question_id)
    
    # Add evaluation
    evaluation = True
    debug_path = "/path/to/debug/log"
    evaluation_id = db_manager.add_evaluation(evaluation, debug_path, rubric_id, response_id)
    
    # Verify evaluation was added
    cursor = db_manager.cursor
    cursor.execute("""
        SELECT evaluation, debug_path, rubric_id, response_id 
        FROM EVALUATION WHERE id = ?
    """, (evaluation_id,))
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == evaluation
    assert result[1] == debug_path
    assert result[2] == rubric_id
    assert result[3] == response_id

def test_delete_question(db_manager):
    """Test deleting a question and related entries"""
    # Setup test data
    question_id = db_manager.add_question("Test question")
    rubric_id = db_manager.add_rubric("Test rubric", question_id, 1)
    response_id = db_manager.add_response("Test response", question_id)
    db_manager.add_evaluation(True, "debug_path", rubric_id, response_id)
    
    # Delete question
    db_manager.delete_question(question_id)
    
    # Verify deletion
    cursor = db_manager.cursor
    cursor.execute("SELECT * FROM QUESTION WHERE id = ?", (question_id,))
    assert cursor.fetchone() is None
    
    cursor.execute("SELECT * FROM RUBRIC WHERE question_id = ?", (question_id,))
    assert cursor.fetchone() is None
    
    cursor.execute("SELECT * FROM RESPONSE WHERE question_id = ?", (question_id,))
    assert cursor.fetchone() is None

def test_get_evaluations_for_response(db_manager):
    """Test retrieving evaluations for a specific response"""
    # Setup test data
    question_id = db_manager.add_question("Test question")
    rubric_id = db_manager.add_rubric("Test rubric", question_id, 1)
    response_id = db_manager.add_response("Test response", question_id)
    evaluation_id = db_manager.add_evaluation(True, "debug_path", rubric_id, response_id)
    
    # Get evaluations
    evaluations = db_manager.get_evaluations_for_response(response_id)
    
    assert len(evaluations) == 1
    evaluation = evaluations[0]
    assert evaluation[0] == evaluation_id  # id
    assert evaluation[1] == True  # evaluation
    assert evaluation[2] == "debug_path"  # debug_path
    assert evaluation[3] == rubric_id
    assert evaluation[4] == response_id

def test_context_manager():
    """Test that the context manager properly closes the connection"""
    db_path = "test_context.db"
    
    with DatabaseManager(db_path) as db:
        # Perform some operation
        db.add_question("Test question")
        
        # Verify connection is working
        try:
            db.cursor.execute("SELECT 1")
            assert True
        except sqlite3.Error:
            assert False, "Connection should be open"
    
    # Try to use the connection after context manager
    # It should raise an error because connection is closed
    with pytest.raises(sqlite3.Error):
        db.cursor.execute("SELECT 1")
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)
        os.remove(db.db_path)