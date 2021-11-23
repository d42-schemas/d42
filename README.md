# d42

[![PyPI](https://img.shields.io/pypi/v/d42.svg?style=flat-square)](https://pypi.python.org/pypi/d42/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/d42?style=flat-square)](https://pypi.python.org/pypi/d42/)
[![Python Version](https://img.shields.io/pypi/pyversions/d42.svg?style=flat-square)](https://pypi.python.org/pypi/d42/)

One package for [district42 ecosystem](https://github.com/topics/district42)

d42 = [district42](https://pypi.org/project/district42/) + [blahblah](https://pypi.org/project/blahblah/) + [valera](https://pypi.org/project/valera/) + [revolt](https://pypi.org/project/revolt/)

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
