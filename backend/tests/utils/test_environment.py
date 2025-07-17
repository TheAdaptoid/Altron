import pytest
from unittest import mock
from src.utils.environment import load_env_var


@mock.patch("src.utils.environment.load_dotenv")
@mock.patch("src.utils.environment.getenv")
def test_load_env_var_returns_value(mock_getenv, mock_load_dotenv):
    mock_getenv.return_value = "test_value"
    result = load_env_var("TEST_VAR")
    mock_load_dotenv.assert_called_once()
    mock_getenv.assert_called_once_with("TEST_VAR")
    assert result == "test_value"


@mock.patch("src.utils.environment.load_dotenv")
@mock.patch("src.utils.environment.getenv")
def test_load_env_var_raises_when_missing(mock_getenv, mock_load_dotenv):
    mock_getenv.return_value = None
    with pytest.raises(ValueError) as excinfo:
        load_env_var("MISSING_VAR")
    assert "Environment variable 'MISSING_VAR' not found." in str(excinfo.value)
