# Playwright QA Framework

End-to-end UI test framework for [Sauce Demo](https://www.saucedemo.com), built with Python, Pytest and Playwright using the Page Object Model.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

## Run
```bash
pytest                              # all tests, headless Chromium
pytest --headed                     # watch the browser
pytest -m smoke                     # smoke tests only
pytest -n 4                         # parallel
pytest --browser firefox --browser webkit   # cross-browser
```
Reports land in `reports/report.html`; screenshots, videos and traces for failures in `test-results/`.

View a trace: `playwright show-trace test-results/<test>/trace.zip`

## Structure
- `pages/` page objects
- `tests/ui/` UI tests
- `test_data/` test data
- `conftest.py` shared fixtures
