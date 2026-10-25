# Contributing

Thanks for contributing to Finsearch-24.

## Setup

1. Create a virtual environment.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

3. Run the test suite:

```bash
python -m pytest -q
```

## Workflow

- Create a feature branch.
- Keep changes focused and easy to review.
- Prefer small, well-documented commits.
- Add or update tests when changing model logic or data handling.
- Run the relevant test suite before submitting a pull request.

## Pull request expectations

- Describe the problem and the fix clearly.
- Include verification evidence when possible.
- Do not regenerate large outputs or add irrelevant files.
