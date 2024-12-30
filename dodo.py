import pytest

DOIT_CONFIG = {"continue": True}

project_name = "koozie"


def task_check_code():
    """Run linter(s)"""
    checkers = ["pylint", "mypy", "black --check"]
    source_checking_paths = [project_name, "test"]

    for checker in checkers:
        for path in source_checking_paths:
            command = f"{checker} {path}"
            if checker == "pylint":
                # Get around weird issue on Windows
                command += "/*.py"
            yield {
                "name": f"{checker} {path}",
                "actions": [command],
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
