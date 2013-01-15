# Harvest

## Install

```bash
$ pip install harvest
```

## Harvest CLI

### Start A New Project

```bash
$ harvest init [--verbose] [--no-env] [--no-input] project_name
```

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


This command performs the following steps:

- Create a new virtualenv environment (name `project_name`-env)
- Installs Django
- Creates a starter project using the built-in Harvest template
- Installs the base dependencies
- Syncs and migrates a SQLite database, this requires you to answer a couple
prompts (unless `--no-input` is passed)
- Collects the static CSS and JavaScript files (mainly due to Cilantro)
- Prints out a message to perform a couple commands in your shell

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
