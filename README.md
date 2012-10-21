# Harvest

## Install

```python
pip install harvest
```

## Harvest CLI

### Start A New Project

```python
harvest init myproject
```

This command performs the following steps:

- Create a new virtualenv environment (name myproject-env)
- Install Django
- Create a starter project structure using the built-in Harvest template
- Install the base dependencies
- Sync and migrate a SQLite database, this requires you to answer a couple
prompts
- Collect the static files (mainly due to Cilantro)
