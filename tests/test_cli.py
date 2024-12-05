import argparse
from pathlib import Path
from unittest.mock import patch

import pytest

from dupehunter.cli import cli_entry_point, parse_arguments


@pytest.fixture
def mock_valid_args():
    """Fixture for valid arguments."""
    return [
        "--base-path",
        "/test/base",
        "--target-path",
        "/test/target",
        "--db-path",
        "/test/db.sqlite",
        "--log-level",
        "INFO",
    ]


def test_parse_arguments_valid(mock_valid_args):
    """Positive test: Parse valid arguments."""
    with patch("sys.argv", ["cli.py"] + mock_valid_args):
        args = parse_arguments()
        assert args.base_path == Path("/test/base")
        assert args.target_path == Path("/test/target")
        assert args.db_path == Path("/test/db.sqlite")
        assert args.log_level == "INFO"


def test_parse_arguments_missing_required():
    """Negative test: Missing required arguments."""
    with patch("sys.argv", ["cli.py", "--base-path", "/test/base"]):
        with pytest.raises(SystemExit):
            parse_arguments()


def test_parse_arguments_invalid_log_level():
    """Negative test: Invalid log level."""
    with patch(
        "sys.argv",
        [
            "cli.py",
            "--base-path",
            "/test/base",
            "--target-path",
            "/test/target",
            "--log-level",
            "INVALID",
        ],
    ):
        with pytest.raises(SystemExit):
            parse_arguments()


@patch("dupehunter.cli.main")
@patch("dupehunter.cli.configure_logging")
@patch("dupehunter.cli.parse_arguments")
def test_cli_entry_point_success(
    mock_parse_args, mock_configure_logging, mock_main, mock_valid_args
):
    """Positive test: Complete CLI flow with mocked dependencies."""
    mock_parse_args.return_value = argparse.Namespace(
        base_path=Path("/test/base"),
        target_path=Path("/test/target"),
        db_path=Path("/test/db.sqlite"),
        log_level="INFO",
    )
    cli_entry_point()
    mock_parse_args.assert_called_once()
    mock_configure_logging.assert_called_once_with("INFO")
    mock_main.assert_called_once_with(
        Path("/test/base"), Path("/test/target"), Path("/test/db.sqlite")
    )


@patch("dupehunter.cli.main", side_effect=Exception("Mocked exception"))
@patch("dupehunter.cli.configure_logging")
@patch("dupehunter.cli.parse_arguments")
def test_cli_entry_point_exception(mock_parse_args, mock_configure_logging, mock_main):
    """Negative test: Simulate an exception in the CLI flow."""
    mock_parse_args.return_value = argparse.Namespace(
        base_path=Path("/test/base"),
        target_path=Path("/test/target"),
        db_path=Path("/test/db.sqlite"),
        log_level="INFO",
    )
    with pytest.raises(Exception, match="Mocked exception"):
        cli_entry_point()
    mock_parse_args.assert_called_once()
    mock_configure_logging.assert_called_once_with("INFO")
    mock_main.assert_called_once_with(
        Path("/test/base"), Path("/test/target"), Path("/test/db.sqlite")
    )
