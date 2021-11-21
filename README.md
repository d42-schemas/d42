# d42

[![PyPI](https://img.shields.io/pypi/v/d42.svg?style=flat-square)](https://pypi.python.org/pypi/d42/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/d42?style=flat-square)](https://pypi.python.org/pypi/d42/)
[![Python Version](https://img.shields.io/pypi/pyversions/d42.svg?style=flat-square)](https://pypi.python.org/pypi/d42/)

## Installation

```sh
pip3 install d42
```

## Usage

```python
from d42 import schema, fake, validate_or_fail

sch = schema.str("banana")

assert validate_or_fail(sch, fake(sch))
```
