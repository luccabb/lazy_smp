
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

`pypy3 -m pip install -r requirements.txt`
### Starting server

`pypy3 main.py`

## Running Tests

### Unit Tests

`python -m unittest tests/test.py`
### Bratko-Kopec Test

`python -m tests.test_bratko_kopec`

## Lichess-bot Python Bridge

This engine implements the UCI protocol and can be used as a bot on [Lichess](https://lichess.org). You can use the python bridge between Lichess Bot API and the engine: [https://github.com/ShailChoksi/lichess-bot](https://github.com/ShailChoksi/lichess-bot). 

To run it as a bot you'll need to produce a python executable. [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/) can produce it by running the following command:

`python3 -m PyInstaller main.py`

This command will produce a `build` and `dist` folder. The `dist` folder contains the main executable in a folder called `main`. All the files inside the `main` folder need to be added under `/lichess-bot/engines` for it to work.
