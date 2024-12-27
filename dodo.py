import pytest

DOIT_CONFIG = {"continue": True}

project_name = "koozie"


def task_check_code():
    """Run linter(s)"""
    checkers = ["pylint", "mypy", "black --check"]
    source_checking_paths = [project_name, "test/*.py"]

    for checker in checkers:
        for path in source_checking_paths:
            yield {
                "name": f"{checker} {path}",
                "actions": [f"{checker} {path}"],
                "verbosity": 1,  # print only errors
            }


def run_pytest():
    """Run pytest"""
    return not bool(pytest.main(["-v", "-s", "test"]))


def task_test():
    """Performs tests"""
    return {
        "actions": [(run_pytest, [])],
        "verbosity": 2,  # print everything
    }


def task_run_cli():
    """Run the CLI"""
    return {
        "actions": ["koozie -l"],
        "verbosity": 1,  # print only errors
    }
