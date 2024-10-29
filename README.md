# d42

[![Codecov](https://img.shields.io/codecov/c/github/d42-schemas/d42/master.svg?style=flat-square)](https://codecov.io/gh/d42-schemas/d42)
[![PyPI](https://img.shields.io/pypi/v/d42.svg?style=flat-square)](https://pypi.python.org/pypi/d42/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/d42?style=flat-square)](https://pypi.python.org/pypi/d42/)
[![Python Version](https://img.shields.io/pypi/pyversions/d42.svg?style=flat-square)](https://pypi.python.org/pypi/d42/)

The `d42` package is a comprehensive toolkit for data modeling, which includes functionalities for definition, generation, validation, and substitution of data models using a robust data description language.

## Installation

```shell
$ pip3 install d42
```

## Usage Example

```python
from d42 import schema, fake, validate_or_fail

# Define a schema for a string containing "banana"
sch = schema.str("banana")

# Generate a fake value based on the schema and validate it
assert validate_or_fail(sch, fake(sch))
```

## Documentation

For detailed documentation, visit the [official d42 documentation](https://d42.sh).
