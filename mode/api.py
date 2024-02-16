import ast
from multiprocessing import set_start_method
from typing import Any, Dict

from chess import Board, polyglot
from flask import Flask, request
from flask_cors import CORS, cross_origin

from config import Config
from helper import get_engine

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADER"] = "Content-Type"


def format_response(best_move: str) -> Dict[str, Any]:
    """
    Format the response to be sent back to the client.

    Arguments:
            - best_move: the best move found.

    Returns:
            - response: a dictionary containing the best
                    move and headers (status code, and allowing
                    CORS) to be sent back to the client.
    """
    return {
        "statusCode": 200,
        "body": {"move": best_move},
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET",
        },
    }


@app.route("/")
@cross_origin()
def main_search() -> Dict[str, Any]:
    """
    Main search route. We'll first search on our opening
    book and if we can't find the move, we'll search using
    the engine.

    The client will send a GET
    request to this route with the following parameters:
            - fen: the fen of the board.
            - depth: the depth to search.
            - null_move: if we're using null move pruning.
                    Options: True, False.
            - algorithm: the algorithm to use. Can be one of
                    the enumerations in the Algorithm class in
                    helper.py.

    Returns:
            - response: a dictionary containing the best
                    move and headers (status code, and allowing
                    CORS) to be sent back to the client.
    """
    # get the parameters from the request
    fen = request.args.get("fen")
    depth = int(request.args.get("depth", 4))
    quiescence_search_depth = int(request.args.get("quiescence_search_depth", 3))
    null_move = ast.literal_eval(str(request.args.get("null_move")))
    null_move_r = int(request.args.get("null_move_r", 2))
    algorithm = request.args.get("algorithm", "alpha_beta")

    config = Config(
        mode="api",
        algorithm=algorithm,
        negamax_depth=depth,
        null_move=null_move,
        null_move_r=null_move_r,
        quiescence_search_depth=quiescence_search_depth
    )

    # create the board
    board = Board(fen)

    # try using cerebellum opening book: https://zipproth.de/Brainfish/download/
    # if it fails we search on our engine. The first (12-20) moves should be
    # available in the opening book, so our engine starts playing after that.
    try:
        best_move = (
            polyglot.MemoryMappedReader("opening_book/cerebellum.bin")
            .find(board)
            .move
            .uci()
        )
    except:
        engine = get_engine(config)
        best_move = engine.search_move(board, depth, null_move).uci()

    return format_response(best_move)


def main():
    """
    Main function to start listening engine.
    """
    # start listening on local host
    app.run(host="0.0.0.0", port=5000, debug=True)
    set_start_method("chess")
