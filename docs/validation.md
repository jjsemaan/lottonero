# **6.1. Validation**

## **6.1.1. Table of Contents - Validation**

- [**6.1.1. Table of Contents - Validation**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#611-table-of-contents---validation)
- [**6.1.2. PEP8 Validation**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#612-pep8-validation)
- [**6.1.3. HTML Validation**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#613-html-validation)
- [**6.1.4. CSS Validation**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#614-css-validation)
- [**6.1.5. JS Validation**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#615-js-validation)
- [**6.1.6. WAVE Validation**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#616-wave-validation)
- [**6.1.7. Lighthouse**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#617-lighthouse)

## **6.1.2. PEP8 Validation**

- **Task :** To ensure `*.py` files are compliant with PEP8 standards.
- **Tools :** 
  - [Black](https://black.readthedocs.io/en/stable/) - PY linter and formatter
  - [CI Python Linter](https://pep8ci.herokuapp.com/) - Visualizing PY linter
- **Method :** 
   - Install `Black` using `pip install black` in terminal
   - Use command `black --line-length 79 DIRECTORY_NAME/` to format `*.py` files in the selected directory or use `black --line-length 79 .` to format all files. Some files were not fully formatted and were left over 79 characters as some errors appeared when formatted due to code complexity.
   - Double check the results in `CI Python Linter` by copying and pasting the Python code as black doesn't wrap lines of comments. 
- **Results :**
The only file failing the PEP8 standard is `lottonero/settings.py` due length of lines of module names.

| Directory            | File                 | Result                   | Remarks                   |
| -------------------- | -------------------- | ------------------------ | ------------------------- |
| \contact             | `admin.py`           | PASS                     |                           |
| \contact             | `forms.py`           | PASS                     |                           |
| \contact             | `models.py`          | PASS                     |                           | 
| \contact             | `urls.py`            | PASS                     |                           |
| \contact             | `views.py`           | PASS                     |                           |
| \home                | `urls.py`            | PASS                     |                           |
| \home                | `views.py`           | PASS                     |                           | 
| \lottery_stats       | `urls.py`            | PASS                     |                           |
| \lottery_stats       | `views.py`           | PASS                     |                           |
| \orders              | `admin.py`           | PASS                     |                           |
| \orders              | `handler.py`         | PASS                     |                           |
| \orders              | `models.py`          | PASS                     |                           |
| \orders              | `urls.py`            | PASS                     |                           |
| \orders              | `views.py`           | FAIL                     | Complex code              |
| \orders              | `webhook.py`         | FAIL                     | Only one line > 79        |
| \Lottonero           | `settings.py`        | FAIL                     | File too delicate         |
| \predictions         | `admin.py`           | PASS                     |                           |
| \predictions         | `forms.py`           | PASS                     |                           |
| \predictions         | `models.py`          | PASS                     |                           |
| \predictions         | `urls.py`            | PASS                     |                           |
| \predictions         | `views.py`           | PASS                     |                           |
| \scraping            | `admin.py`           | PASS                     |                           |
| \scraping            | `models.py`          | PASS                     |                           |
| \scraping            | `urls.py`            | PASS                     |                           |
| \scraping            | `views.py`           | FAIL                     | Complex code              |
| \user_profile        | `urls.py`            | PASS                     |                           |
| \user_profile        | `views.py`           | PASS                     |                           |

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#611-table-of-contents---validation)

[Back to README.md](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

## **6.1.3. HTML Validation**

- **Task :** To ensure source code generated from all `*.html` templates is compliant with W3C standards.
- **Tools :** 
  - [W3C HTML Validator](https://validator.w3.org/) - HTML Validator
- **Method :** 
   - Open each page of the project
   - In Chrome : Right click on page background and select `View Page Source`
   - Copy and Paste the generated code from browser to validator
   - See results *( Appendix 82 )*
   - Please note this needs to be done for all states of the templates (i.e. Logged In / Logged Out, Empty Vault/Items in Vault etc.)
- **Results :**

| Directory           | File                         | State             | Warnings | Errors | Nature of Problem                                    | Result |
| ------------------- | ---------------------------- | ----------------- | -------- | ------ | ---------------------------------------------------- | ------ |
| \\home              | `index.html`                 | Not Applicable    | 4        | 3      | Navigation should have been separated from base.html | FAIL   |
| \\home              | `alltime.html`               | Not Applicable    | 4        | 1      | Navigation should have been separated from base.html | FAIL   |
| \\home              | `alltime_shuffled.html`      | Not Applicable    | 4        | 1      | Navigation should have been separated from base.html | FAIL   |