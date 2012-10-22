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

_`project_name` must be a valid Python identifier which means it can
only contain alphanumeric characters and underscores and cannot start
with a number._

This command performs the following steps:

- Create a new virtualenv environment (name myproject-env)
- Install Django
- Create a starter project structure using the built-in Harvest template
- Install the base dependencies
- Sync and migrate a SQLite database, this requires you to answer a couple
prompts (unless `--no-input` is passed)
- Collect the static files (mainly due to Cilantro)

**Options**

`--verbose` - Pass to get all output printed to stdout.

`--no-env` - Pass to prevent creating a virtualenv. If set, it is assumed the
virtualenv is active prior to running this command to ensure dependencies are
installed in the correct site-packages directory.

`--no-input` - Pass to prevent being prompted during the setup. This
currently includes the prompt for setting up a superuser during the database
sync. This is primarily useful for performing scripted builds.

### Update Harvest

```bash
$ harvest update
```
