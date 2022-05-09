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
    session.run(
        "flake8",
        ".",
        "--count",
        "--max-line-length=127",
        # Exclude '.nox/' to avoid unrelated errors (from the created venv)
        "--exclude=.nox/",
        # Ignore the following errors, since they come from star imports.
        # TODO: Remove this workaround at some point!
        "--ignore=F403,F405",
        "--show-source",
        "--statistics",
    )
    session.run("isort", ".", "--check-only", "-v")
    session.run("black", "--check", ".")


@nox.session
def format(session):
    "Run formatters."
    session.install("-r", "requirements-dev.txt")
    session.run("isort", ".", "-v")
    session.run("black", ".")
