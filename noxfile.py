"""
Developers feature: Nox settings
to ease your hard work.
"""

import nox

nox.options.sessions = ["format", "lint"]

@nox.session
def lint(session):
    "Run linters, just to check quality."
    session.install("-r", "requirements-dev.txt")
    session.run("flake8", ".", "--count", "--max-complexity=10", "--max-line-length=127", "--show-source", "--statistics")
    session.run("isort", ".", "--check-only", "-v")
    session.run("black", "--check", ".")


@nox.session
def format(session):
    "Run formatters."
    session.install("-r", "requirements-dev.txt")
    session.run("isort", ".", "-v")
    session.run("black", ".")
