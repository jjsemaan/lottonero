# **6.1. Validation**

## **6.1.1. Table of Contents - Validation**

- [**6.1.1. Table of Contents - Validation**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#611-table-of-contents---validation)
- [**6.1.2. PEP8 Validation**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#612-pep8-validation)
- [**6.1.3. HTML Validation**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#613-html-validation)
- [**6.1.4. CSS Validation**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#614-css-validation)
- [**6.1.5. Lighthouse**](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#615-lighthouse)

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

| Directory           | File                         | State             | Warnings | Errors | Nature of Problem         | Result |
| ------------------- | ---------------------------- | ----------------- | -------- | ------ | ------------------------- | ------ |
| \\home              | `index.html`                 | Not Applicable    | 0        | 0      |                           | PASS   |
| \\home              | `alltime.html`               | Not Applicable    | 0        | 0      |                           | PASS   |
| \\home              | `alltime_shuffled.html`      | Not Applicable    | 0        | 0      |                           | PASS   |
| \\contact           | `about.html`                 | Not Applicable    | 0        | 0      |                           | PASS   |
| \\contact           | `contact.html`               | Not Applicable    | 0        | 0      |                           | PASS   |
| \\lottery_stats     | `frequencies.html`           | Logged In         | 2        | MULTI  | Plotly syntax not recognised | FAIL   |
| \\lottery_stats     | `correlations.html`          | Logged In         | 2        | MULTI  | Plotly syntax not recognised | FAIL   |
| \\lottery_stats     | `combinations.html`          | Logged In         | 2        | MULTI  | Plotly syntax not recognised | FAIL   |
| \\orders            | `pricing_page.html`          | Logged In         | 0        | 0      |                           | PASS   |
| \\orders            | `confirm_cancel.html`        | Logged In         | 0        | 0      |                           | PASS   |
| \\orders            | `subscription_confirm.html`  | Logged In         | 0        | 0      |                           | PASS   |
| \\predictions       | `backoffice.html`            | Only as Admin     | 0        | 9      | No issues found in reported errors | PASS   |
| \\user_profile      | `privacy_policy.html`        | Not Applicable    | 0        | 0      |                           | PASS   |
| \\user_profile      | `terms_and_conditions.html`  | Not Applicable    | 0        | 0      |                           | PASS   |
| \\user_profile      | `profile.html`               | Not Applicable    | 0        | 0      |                           | PASS   |

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#611-table-of-contents---validation)

[Back to README.md](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **6.1.4. CSS Validation**

My styling files were separated into smaller files by app names for easy navigation.

- **Task :**  To ensure the code in `*.css` is compliant with W3C standards.
- **Tools :** 
  - [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) - CSS Validator
- **Method :** 
   - Open the `*.css` file
   - Copy and Paste the code from IDE to validator
   - See results
- **Results :**

| Directory     | File               | Warnings | Errors | Nature of Problem                     | Result |
| ------------- | ------------------ | -------- | ------ | ------------------------------------- | ------ |
| \\static\\css | `base.css`         | 0        | 0      |                                       | PASS   |

*Appendix 48 - CSS Pass*

![CSS Validation](/docs/css-check.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#611-table-of-contents---validation)

[Back to README.md](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---

## **6.1.5. Lighthouse**

- **Task :** To ensure that speeds of project loading are viable.
- **Tools :** 
  - [Chrome Lighthouse](https://developer.chrome.com/docs/lighthouse/overview) - Chrome Lighthouse documentation
- **Method :** 
   - Browse each page and click on `More Tools > Developer Tools > Lighthouse > Analyze Page Load`
   - See results on the right hand panel
- **Finding :**
  - Performance is 65 , page need improvement towards server response time.
- **Results :**
  - Various suggestions were made between minifying the CSS, reducing unused JS files and others. 

*Appendix 49 - Lighthouse*

![Lighthouse Result](/docs/validation/lighthouse-result.JPG)

[Back to top](https://github.com/jjsemaan/lottonero/blob/main/docs/validation.md#611-table-of-contents---validation)

[Back to README.md](https://github.com/jjsemaan/lottonero/blob/main/README.md#lottonero---portfolio-project-5)

---