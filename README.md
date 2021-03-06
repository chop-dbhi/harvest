# Harvest

[![Build Status](https://travis-ci.org/chop-dbhi/harvest.svg?branch=master)](https://travis-ci.org/chop-dbhi/harvest) [![Coverage Status](https://img.shields.io/coveralls/chop-dbhi/harvest.svg)](https://coveralls.io/r/chop-dbhi/harvest)

## What Is It

- Ad-hoc query engine for relational databases
  - Uses Django to build SQL and execute the query
  - Uses a simple JSON-based DSL for declaring the query
  - Uses metadata index for query evaluation and preparation
  - Does not require knowing how data model components are related
- Modern HTML5 Web client for building and interacting with queries completely driven by a robust REST API
- Save queries for future reference
- Share queries for increased knowledge dissemination
- Export data into CSV, Excel, and JSON formats
  - Export an R or SAS bundles containing the data and script for streamlined data analysis
- Persisted metadata index of the relational data model
  - Relies on pre-defined Django models to build metadata index
- User-centric annotations on metadata for improved domain specificity
- Lightweight "concept" model for improving how fields in a data model are presented for query or viewing purposes
  - Abstraction used for presentation which is a translation between raw data model and end user.
    - Descriptors
    - Custom query interface
    - Custom output

## Install

```bash
$ pip install harvest
```

## Harvest CLI

### Dependencies

This version of Harvest requires Python 2.6 or 2.7.

### Start A New Project

```bash
$ harvest init [--verbose] [--no-env] [--no-input] project_name
```
This command performs the following steps:

- Create a new virtualenv environment (name `project_name`-env)
- Installs Django
- Creates a starter project using the built-in Harvest template
- Installs the base dependencies
- Syncs and migrates a SQLite database, this requires you to answer a couple
prompts (unless `--no-input` is passed)
- Collects the static CSS and JavaScript files (mainly due to Cilantro)
- Prints out a message to perform a couple commands in your shell

**Arguments**

`project_name` - The name of the project which must be a valid Python
identifier since it will be an importable Python package. This means it can
only contain alphanumeric characters and underscores and cannot start with a
number, such as `myproject`, `my_project`, and `project1`, but not `1project`,
`my-project` or `-myproject`.

**Options**

`--verbose` - Pass to get all output printed to stdout. Multiple flags can be
passed to increase the verbosity, e.g. `-vv`.

`--no-env` - Pass to prevent creating a virtualenv. If set, it is assumed the
virtualenv is active prior to running this command to ensure dependencies are
installed in the correct site-packages directory.

`--no-input` - Pass to prevent being prompted during the setup. This
currently includes the prompt for setting up a superuser during the database
sync. This is primarily useful for performing scripted builds.

`--template` - Specify a template to base your Harvest application on. By
default `harvest init` will base its build off of
`https://github.com/cbmi/harvest-template/archive/HEAD.zip`. By passing a URL to
this option `harvest init` will attempt to bootstrap the project based on the
endpoint specified. Additionally, if your provided template contains a Fabric
fabfile containing a `harvest_bootstrap` task the init command will offload all
bootstrapping tasks beyond creating the virtualenv and installing of
dependencies to the `harvest_bootstrap` task. This could be useful in situations
where further assumptions can be made about a new Harvest deployment
(i.e. containerization, use of a specific DB, specific Django models, etc.).

`--venv-wrap` - If you are using virtualenvwrapper to handle your python virtual
environments you can set this flag to create a virtualenv in accordance with
the conventions of that utility -- The name of your environment will correspond
to your project name and will be created in the directory specified by the
`WORKON_HOME` environment variable.

**Post-Setup**

After creating a new Harvest project, the next step is to define a few Django
models. Run `python bin/manage.py avocado check` to see what needs to be
further setup as well as optional settings and dependencies that can be
installed.

### Update Harvest

This command updates itself to the lastest stable version from PyPi.

```bash
$ harvest update
```

### Install Demo

This command installs one of the Harvest demos.

```bash
$ harvest init-demo [--verbose] [--no-env] demo_name
```

**Arguments**

`demo_name` - The name of an available demo which is currently only `openmrs`.

**Options**

`--verbose` - Pass to get all output printed to stdout. Multiple flags can be
passed to increase the verbosity, e.g. `-vv`.

`--no-env` - Pass to prevent creating a virtualenv. If set, it is assumed the
virtualenv is active prior to running this command to ensure dependencies are
installed in the correct site-packages directory.
