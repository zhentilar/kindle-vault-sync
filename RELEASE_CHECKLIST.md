# Release Checklist

Use this checklist before making the repository public.

## 1. Security and Privacy

- [ ] Confirm .env is listed in .gitignore.
- [ ] Confirm no real credentials are committed.
- [ ] Search repository for secrets:
  - [ ] KVS_APP_PASSWORD
  - [ ] KVS_SENDER_EMAIL
  - [ ] KVS_KINDLE_EMAIL
- [ ] Verify config examples contain only placeholder values.
- [ ] Verify no private vault paths are hardcoded.

## 2. Project Metadata

- [ ] Confirm project name and description in pyproject.toml.
- [ ] Confirm author metadata is generic/public-safe.
- [ ] Confirm version is updated (semantic versioning).
- [ ] Confirm LICENSE is present and correct.

## 3. Local Validation

- [ ] Create a clean virtual environment.
- [ ] Install package in editable mode.
- [ ] Run tests: pytest -q
- [ ] Run preview command with a sample config.
- [ ] Verify HTML output is generated in output directory.

## 4. Documentation Quality

- [ ] README Quick Start runs without missing steps.
- [ ] README includes environment variable setup.
- [ ] README includes preview and send command examples.
- [ ] README includes configuration reference for all fields.
- [ ] Add one sample screenshot/output block if desired.

## 5. CI and Repository Hygiene

- [ ] CI workflow passes on main branch.
- [ ] Repo has a clear default branch (main).
- [ ] Add topics/tags on GitHub for discoverability.
- [ ] Optional: add issue templates.
- [ ] Optional: add CODE_OF_CONDUCT.md and CONTRIBUTING.md.

## 6. First Public Release Steps

- [ ] Initialize git repo if needed.
- [ ] Commit files with clear message.
- [ ] Push to GitHub.
- [ ] Set repository visibility to Public.
- [ ] Create first release tag (for example v0.1.0).
- [ ] Add release notes with key features.

## 7. Post-Publish

- [ ] Verify README renders correctly on GitHub.
- [ ] Verify links to files and workflow are valid.
- [ ] Open one test issue to validate issue flow.
- [ ] Share repository URL.
