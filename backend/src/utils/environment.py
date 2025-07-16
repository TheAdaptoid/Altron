from os import getenv

from dotenv import load_dotenv


def load_env_var(var_name: str) -> str:
    """Loads the value of the specified environment variable.

    This function loads environment variables from a .env file (if present) and retrieves
    the value of the given environment variable name. If the variable is not found,
    a ValueError is raised.

    Args:
        var_name (str): The name of the environment variable to retrieve.

    Returns:
        str: The value of the specified environment variable.

    Raises:
        ValueError: If the environment variable is not found.
    """
    load_dotenv()

    env_var: str | None = getenv(var_name)

    if not env_var:
        raise ValueError(f"Environment variable '{var_name}' not found.")

    return env_var
