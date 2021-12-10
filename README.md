
## Requirements

```
python
pypy3
pip
```
## Running server
### Installing dependencies

`pip install -r requirements.txt`

### Starting server

`python main.py`
## Running with pypy

### Installing dependencies

1. Make sure that you have pip for pypy

`pypy3 -m ensurepip`

2. Install dependencies
`pypy3 -m pip install -r requirements_pypy.txt`
### Starting server

`pypy3 main_pypy.py`

## Running Tests

### Unit Tests

`python -m unittest test.py`
### Bratko-Kopec Test

`python test_bratko_kopec.py`