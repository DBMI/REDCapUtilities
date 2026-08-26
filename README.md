# REDCapUtilities ![image info](./pictures/logo.png) 

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Coverage Status](./.github/badges/coverage-badge.svg?dummy=8484744)
![GitHub last commit](https://img.shields.io/github/last-commit/dbmi/REDCapUtilities)

---

**Documentation**: [https://dbmi.github.io/REDCapUtilities/](https://dbmi.github.io/REDCapUtilities/)

**Source Code**: [https://github.com/DBMI/REDCapUtilities](https://github.com/DBMI/REDCapUtilities)

---
## Purpose

The REDCapUtilities library contains functions used across more than one project.

### Address Standardization
A patient may have their address listed in one database as _123 N Apple St #234_ and in another database as _123 North Apple Street Apt 234_. To help recognize these strings as the same address, the `AddressStandardizer` class uses the Python package [usaddress](https://pypi.org/project/usaddress/) to break up an address string into its components (like _AddressNumber_, _StreetNamePreDirectional_, etc.), then applies the [US Postal service rules](https://pe.usps.com/text/pub28/welcome.htm) that (for example) turn "North" into "N" and "Street" into "ST".


### String Cleanup
#### Dates
Patient birth dates could be recorded in any number of formats, making it difficult for software to recognize that "2001-02-03" is the same as "February 3, 2001." The method `clean_up_date` uses the Python package `dateutil.parser` to parse suspected date/time strings into `datetime` objects, then convert them to `%Y-%m-%d` format.

#### Email Addresses
Sometimes patient email address fields contain notes like "declined" or "unknown". It's misleading to say two patient records have matching email addresses when really both say "unknown". The method `clean_up_email` removes notes like "declined", "none" etc. to make later email comparisons valid.

#### Language
If a patient's preferred language field says "Other" or "Unknown", we'd rather it be blank. The method `clean_up_language` converts these nonsense values to blank strings.

#### Phone Number
The method `clean_up_phone`:
- removes non-numeric characters
- removes nonsense values like "NONE", "0000000000" or "619-000-0000"
- strips off leading "1" characters (as in "1-629-555-1212")
- rebuilds the number in ###-###-#### format.

#### Time
The method `clean_up_time` uses the Python package `dateutil.parser` to parse suspected date/time strings into `datetime` objects, then convert them to `%H:%M:%S` format.

## Installation

```sh
pip install git+https://github.com/DBMI/REDCapUtilities.git
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.7+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github project page
 ](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/DBMI/REDCapUtilities/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/DBMI/REDCapUtilities/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/DBMI/REDCapUtilities/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using the [python-package-cookiecutter](https://github.com/DBMI/python-package-cookiecutter) template, modeled on the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
