import chess
import chess.polyglot
from flask import request
from flask_cors import CORS, cross_origin
from flask import Flask
from helper import get_engine
from typing import Dict, Any
from multiprocessing import set_start_method


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'


def format_response(best_move: str) -> Dict[str, Any]:
	return {
		'statusCode': 200,
		'body': {'move': best_move},
		'headers': {
			'Access-Control-Allow-Headers': 'Content-Type',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,GET'
		},
	}


@app.route('/')
@cross_origin()
def main_search() -> Dict[str, Any]:
	fen = request.args.get('fen')
	board = chess.Board(fen)

	# ALGORITHM_NAME =  "alpha_beta"
	# ALGORITHM_NAME = "parallel_alpha_beta_layer_1"
	ALGORITHM_NAME = "parallel_alpha_beta_layer_2"
	# ALGORITHM_NAME = "lazy_smp"
	DEPTH = 3
	NULL_MOVE = True

	engine = get_engine(ALGORITHM_NAME)
	
	# using cerebellum opening book: https://zipproth.de/Brainfish/download/
	try:
		best_move = chess.polyglot.MemoryMappedReader("opening_book/cerebellum.bin").weighted_choice(board).move().uci()
	except:
		best_move = engine(board, DEPTH, NULL_MOVE)
	
	return format_response(best_move)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)
	set_start_method("chess")
