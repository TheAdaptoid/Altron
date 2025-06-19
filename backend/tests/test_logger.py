import logging
from collections.abc import Generator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.utils import setup_logger


@pytest.fixture
def temp_log_dir(tmp_path: Path) -> Generator[Path, Any, None]:
    """Create a temporary log directory for testing."""
    temp_dir = tmp_path / "logs"
    temp_dir.mkdir()

    # Patch the log directory
    with patch("src.utils.logger.log_dir", temp_dir):
        yield temp_dir


@pytest.fixture
def mock_settings() -> Generator[MagicMock, Any, None]:
    """Mock settings for testing different debug modes."""
    with patch("src.utils.logger.settings") as mock_settings:
        yield mock_settings


def test_setup_logger_creates_handlers() -> None:
    """Test that setup_logger creates both console and file handlers."""
    logger = setup_logger("test_logger")

    assert isinstance(logger, logging.Logger)
    assert len(logger.handlers) == 2
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
    assert any(isinstance(h, logging.FileHandler) for h in logger.handlers)


def test_setup_logger_debug_mode(mock_settings: MagicMock) -> None:
    """Test logger configuration in debug mode."""
    mock_settings.DEBUG = True
    logger = setup_logger("test_debug_logger")

    assert logger.level == logging.DEBUG
    assert any(h.level == logging.DEBUG for h in logger.handlers)


def test_setup_logger_production_mode(mock_settings: MagicMock) -> None:
    """Test logger configuration in production mode."""
    mock_settings.DEBUG = False
    logger = setup_logger("test_prod_logger")

    assert logger.level == logging.INFO
    assert all(h.level >= logging.INFO for h in logger.handlers)


def test_setup_logger_creates_log_file(temp_log_dir: Path) -> None:
    """Test that setup_logger creates a log file."""
    logger = setup_logger("test_file_logger")
    log_file = temp_log_dir / "app.log"

    # Log a test message
    test_message = "Test log message"
    logger.info(test_message)

    assert log_file.exists()
    assert test_message in log_file.read_text()


def test_setup_logger_reuses_existing_logger() -> None:
    """Test that setup_logger doesn't create duplicate handlers."""
    logger1 = setup_logger("test_reuse_logger")
    initial_handler_count = len(logger1.handlers)

    logger2 = setup_logger("test_reuse_logger")
    assert logger1 is logger2
    assert len(logger2.handlers) == initial_handler_count
