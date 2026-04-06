# Contributing

Thanks for contributing to Kindle Vault Sync.

## Development Setup

1. Create and activate a virtual environment.
2. Install project and test dependencies.
3. Run tests before opening a pull request.

Example (fish shell):

- python3 -m venv .venv
- source .venv/bin/activate.fish
- pip install -e . pytest
- pytest -q

## Branch and Commit Guidelines

- Create a feature branch from main.
- Keep changes focused and small.
- Write clear commit messages.
- Update docs when behavior changes.

## Pull Request Checklist

- [ ] Tests pass locally.
- [ ] README/config docs updated if needed.
- [ ] No secrets or private paths added.
- [ ] Backward compatibility considered.

## Code Style

- Prefer readable, small functions.
- Add brief comments only for non-obvious logic.
- Keep public CLI behavior stable unless documented.

## Reporting Issues

Use the issue templates for bug reports and feature requests.
