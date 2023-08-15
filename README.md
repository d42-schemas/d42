# d42

[![PyPI](https://img.shields.io/pypi/v/d42.svg?style=flat-square)](https://pypi.python.org/pypi/d42/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/d42?style=flat-square)](https://pypi.python.org/pypi/d42/)
[![Python Version](https://img.shields.io/pypi/pyversions/d42.svg?style=flat-square)](https://pypi.python.org/pypi/d42/)

`d42` package offers several tools to define, generate, validate, and substitute data based on models defined using the district42 data description language.

## Installation

```shell
$ pip3 install d42
```

## Components

The [d42](https://pypi.org/project/d42/) package comprises the following components:
- [district42](https://pypi.org/project/district42/) — a data description language for defining data models
- [blahblah](https://pypi.org/project/blahblah/) — a fake data generator tailored for the district42 schema
- [valera](https://pypi.org/project/valera/) — a validator designed for the district42 schema
- [revolt](https://pypi.org/project/revolt/) — a value substitutor compatible with the district42 schema

## Usage

```python
from d42 import schema, fake, validate_or_fail

# Define a schema with a string "banana"
sch = schema.str("banana")

# Generate a fake value based on the schema and validate it
assert validate_or_fail(sch, fake(sch))
```

For a more comprehensive guide and detailed information, check out the [official documentation](https://d42.vedro.io/).
