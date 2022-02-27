# Moonfish Engine ([~2000 Elo Rating Lichess.org](https://lichess.org/@/moonfish_bot))

Didatic Python Chess Engine
## Installing dependencies

```
pip install -r requirements.txt
```
## Running the Engine

### 1. Running as an [UCI](http://wbec-ridderkerk.nl/html/UCIProtocol.html) Compatible Engine

```
python main.py
```

### 2. Running as a Web Server

```
python api.py
```

## Running Tests


### Unit Tests

Unit tests are testing the basic functionality of the engine,
with key positions and moves.

```
python -m unittest tests/test.py
```

### Bratko-Kopec Test

[Bratko-Kopec](https://www.chessprogramming.org/Bratko-Kopec_Test) tests the engine 
performance in terms of time and strenght.

```
python -m tests.test_bratko_kopec
```

## Lichess-bot Python Bridge

This engine implements the UCI protocol and can be used as a bot on [Lichess](https://lichess.org). You can use the python bridge between Lichess Bot API and the engine: [https://github.com/ShailChoksi/lichess-bot](https://github.com/ShailChoksi/lichess-bot). 

To run it as a bot you'll need to produce a python executable. [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/) can produce it by running the following command:

```
python3 -m PyInstaller main.py
```

This creates a `build` and `dist` folder. The `dist` folder contains the main executable in a folder called `main`. All the files inside `main` need to be copied over to `/lichess-bot/engines` for it to work.
