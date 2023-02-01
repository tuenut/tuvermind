import os
import sys

from pydantic import BaseModel

__all__ = [
    "DEBUG", "SECRET_KEY", "TUVERMIND_REDIS_HOST", "TUVERMIND_REDIS_PORT"
]


class AppConfigurationParameters(BaseModel):
    TUVERMIND_DEBUG: bool = False
    TUVERMIND_SECRET_KEY: str = "fake_secret_key"

    @classmethod
    def get_from_env(cls, name):
        return os.environ.get(name, cls.__fields__[name].default)


class AppConfig:
    params_model = AppConfigurationParameters
    config: AppConfigurationParameters

    def __init__(self):
        self.config = self.__get_config_from_env()

    __run_in_test = None

    @property
    def is_run_in_testing(self):
        """
        May be if run `python3 manage.py test` for run tests only.
        Or may run for testing purposes, then looks for env var.
        """
        if self.__run_in_test is None:
            is_runnig_tests = len(sys.argv) > 1 and sys.argv[1] == "test"
            is_run_for_testing = os.environ.get("HELPDESK_RUN_IN_TESTING")
            self.__run_in_test = is_runnig_tests or is_run_for_testing

        return self.__run_in_test

    def __get_config_from_env(self) -> AppConfigurationParameters:
        environmet_vars = {
            name: AppConfigurationParameters.get_from_env(name)
            for name in AppConfigurationParameters.__fields__
        }
        environmet_vars["HELPDESK_RUN_IN_TESTING"] = self.is_run_in_testing

        config = self.params_model(**environmet_vars)

        return config


DEBUG = bool(os.getenv("TUVERMIND_DEBUG", False))

SECRET_KEY = os.getenv("TUVERMIND_SECRET_KEY", None)
API_KEY = os.getenv("TUVERMIND_API_KEY")

TUVERMIND_REDIS_HOST = os.getenv("TUVERMIND_REDIS_HOST")
TUVERMIND_REDIS_PORT = int(os.getenv("TUVERMIND_REDIS_PORT", 6379))

DB_USER = os.getenv("TUVERMIND_DB_USER")
DB_PASSWORD = os.getenv("TUVERMIND_DB_PASSWORD")
DB_HOST = os.getenv("TUVERMIND_DB_HOST")
DB_PORT = os.getenv("TUVERMIND_DB_PORT", 5432)

