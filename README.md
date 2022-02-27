# Moonfish Engine (~2000 Elo Rating Lichess.org)

Didatic Python Chess Engine
## Installing dependencies

`pip install -r requirements.txt`
## Running the Engine

### Running as a Universal Chess Interface (UCI) Engine

`python main.py`
### Running as a web server

`python api.py`

## Running Tests

### Unit Tests

`python -m unittest tests/test.py`
### Bratko-Kopec Test

`python -m tests.test_bratko_kopec`

## Lichess-bot Python Bridge

This engine implements the UCI protocol and can be used as a bot on [Lichess](https://lichess.org). You can use the python bridge between Lichess Bot API and the engine: [https://github.com/ShailChoksi/lichess-bot](https://github.com/ShailChoksi/lichess-bot). 

To run it as a bot you'll need to produce a python executable. [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/) can produce it by running the following command:

`python3 -m PyInstaller main.py`

This creates a `build` and `dist` folder. The `dist` folder contains the main executable in a folder called `main`. All the files inside `main` need to be copied over to `/lichess-bot/engines` for it to work.
