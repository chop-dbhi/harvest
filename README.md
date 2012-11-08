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

This is what you will see (the number of migrations will vary over time):

```
$ harvest init myproject
Setting up a virtual environment 'myproject-env'...
Installing Django...
Creating new Harvest project 'myproject'...
Downloading and installing dependencies...
Collecting static files...
Setting up a SQLite database...
Syncing...
Creating tables ...
Creating table south_migrationhistory
Creating table django_admin_log
Creating table auth_permission
Creating table auth_group_permissions
Creating table auth_group
Creating table auth_user_user_permissions
Creating table auth_user_groups
Creating table auth_user
Creating table django_content_type
Creating table django_session
Creating table django_site

You just installed Django's auth system, which means you don't have any superusers defined.
Would you like to create one now? (yes/no): yes
Username (leave blank to use 'ruthb'): 
E-mail address: ruthb@email.chop.edu
Password: 
Password (again): 
Superuser created successfully.
Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)
Migrating...
Running migrations for cilantro:
 - Migrating forwards to 0003_auto__chg_field_siteconfiguration_site.
 > cilantro:0001_initial
 > cilantro:0002_auto__add_field_siteconfiguration_auth_required
 > cilantro:0003_auto__chg_field_siteconfiguration_site
 - Loading initial data for cilantro.
Installed 0 object(s) from 0 fixture(s)
Running migrations for avocado:
 - Migrating forwards to 0006_add_dataconcept_slugs.
 > avocado:0001_initial
 > avocado:0002_auto__chg_field_dataview_name__chg_field_datafield_name__chg_field_dat
 > avocado:0003_auto__del_field_dataconcept_formatter__add_field_dataconcept_formatter
 > avocado:0004_rename_dataview_concepts_to_columns
 - Migration 'avocado:0004_rename_dataview_concepts_to_columns' is marked for no-dry-run.
 > avocado:0005_auto__add_field_datafield_internal__add_field_dataconcept_ident__add_f
 > avocado:0006_add_dataconcept_slugs
 - Migration 'avocado:0006_add_dataconcept_slugs' is marked for no-dry-run.
 - Loading initial data for avocado.
Installed 0 object(s) from 0 fixture(s)

Synced:
 > myproject
 > south
 > serrano
 > django.contrib.admin
 > django.contrib.auth
 > django.contrib.contenttypes
 > django.contrib.humanize
 > django.contrib.markup
 > django.contrib.messages
 > django.contrib.sessions
 > django.contrib.sites
 > django.contrib.staticfiles

Migrated:
 - cilantro
 - avocado

Complete! Copy and paste the following into your shell:

cd myproject-env/myproject
source ../bin/activate
./bin/manage.py runserver

Open up a web browser and go to: http://localhost:8000
```

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
