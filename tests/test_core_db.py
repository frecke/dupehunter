import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from dupehunter.database import initialize_database, load_catalog


@pytest.fixture
def mock_db_path(tmp_path):
    """Fixture for creating a mock database path."""
    return tmp_path / "test_file_catalog.db"


def test_initialize_database_success(mock_db_path):
    """Positive test: Verify the database is initialized successfully."""
    initialize_database(mock_db_path)
    assert mock_db_path.exists()

    # Verify the database schema
    conn = sqlite3.connect(mock_db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='file_info'"
    )
    table_exists = cursor.fetchone()
    conn.close()
    assert table_exists is not None


def test_initialize_database_existing_db(mock_db_path):
    """Normal test: Verify behavior when the database already exists."""
    # Create the database first
    initialize_database(mock_db_path)
    original_mod_time = mock_db_path.stat().st_mtime

    # Call the function again
    initialize_database(mock_db_path)
    updated_mod_time = mock_db_path.stat().st_mtime

    # Ensure the file's modification time hasn't changed (existing DB remains untouched)
    assert original_mod_time == updated_mod_time


@patch("sqlite3.connect")
def test_initialize_database_custom_path(mock_connect, tmp_path):
    """Alternative test: Test with a custom database path."""
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    custom_path = tmp_path / "custom_db.db"
    initialize_database(custom_path)

    # Verify connect is called with the custom path
    mock_connect.assert_called_once_with(custom_path)

    # Verify the table creation SQL is executed
    mock_cursor.execute.assert_called_once_with(
        """
        CREATE TABLE IF NOT EXISTS file_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE,
            checksum TEXT,
            metadata TEXT,
            file_size INTEGER
        )
        """
    )
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


@patch(
    "sqlite3.connect",
    side_effect=sqlite3.OperationalError("Cannot connect to database"),
)
def test_initialize_database_exception(mock_connect, tmp_path):
    """Exception handling: Simulate a database connection error."""
    db_path = tmp_path / "invalid_db.db"

    with pytest.raises(sqlite3.OperationalError, match="Cannot connect to database"):
        initialize_database(db_path)

    # Verify that connect was attempted
    mock_connect.assert_called_once_with(db_path)


@pytest.mark.parametrize("db_path_suffix", ["file1.db", "file2.db", "file3.db"])
def test_initialize_database_parametrize(db_path_suffix, tmp_path):
    """Parameterized test: Verify database initialization with different paths."""
    db_path = tmp_path / db_path_suffix
    initialize_database(db_path)

    # Verify that the file is created and schema is valid
    assert db_path.exists()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='file_info'"
    )
    table_exists = cursor.fetchone()
    conn.close()
    assert table_exists is not None


@pytest.fixture
def setup_database(mock_db_path):
    """
    Fixture to populate a mock SQLite database with test data.

    Parameters:
        mock_db_path (str): Path to the mock database.

    Yields:
        None: Provides a pre-populated database for testing.
    """
    conn = sqlite3.connect(mock_db_path)
    cursor = conn.cursor()

    # Create the file_info table
    cursor.execute(
        """
        CREATE TABLE file_info (
            file_path TEXT NOT NULL,
            checksum TEXT NOT NULL,
            metadata TEXT,
            file_size INTEGER NOT NULL
        )
        """
    )

    # Insert test data into the table
    test_data = [
        ("/path/to/file1.jpg", "checksum1", '{"Author": "Alice"}', 1024),
        ("/path/to/file2.png", "checksum2", '{"Author": "Bob"}', 2048),
    ]
    cursor.executemany(
        """
        INSERT INTO file_info (file_path, checksum, metadata, file_size)
        VALUES (?, ?, ?, ?)
        """,
        test_data,
    )

    # Commit changes
    conn.commit()

    # Yield to allow test execution with the setup database
    yield

    # Cleanup after test completion
    conn.close()


@pytest.fixture
def setup_empty_database(mock_db_path):
    """Fixture to create an empty database."""
    import sqlite3

    conn = sqlite3.connect(mock_db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE file_info (
            file_path TEXT,
            checksum TEXT,
            metadata TEXT,
            file_size INTEGER
        )
        """
    )
    conn.commit()
    conn.close()


def test_load_catalog_success(mock_db_path, setup_database):
    """Positive test: Verify correct data is loaded from the database."""
    result = load_catalog(mock_db_path)
    expected = [
        {
            "file_path": "/path/to/file1.jpg",
            "checksum": "checksum1",
            "metadata": '{"Author": "Alice"}',
            "file_size": 1024,
        },
        {
            "file_path": "/path/to/file2.png",
            "checksum": "checksum2",
            "metadata": '{"Author": "Bob"}',
            "file_size": 2048,
        },
    ]
    assert result == expected
