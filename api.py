from flask import request
from flask_cors import CORS, cross_origin
from flask import Flask
import chess
import chess.polyglot
import time
import helper
from typing import Dict, Any
import multiprocessing as mp


# Search constants
R = 2
COUNTER = 0

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
	st = time.time()
	fen = request.args.get('fen')
	board = chess.Board(fen)

	# ALGORITHM_NAME =  "alpha_beta"
	# ALGORITHM_NAME = "parallel_alpha_beta_layer_1"
	ALGORITHM_NAME = "parallel_alpha_beta_layer_2"
	# ALGORITHM_NAME = "lazy_smp"

	engine = helper.get_implementation(ALGORITHM_NAME)

	depth = 3
	player = 1
	null_move = True
	
	# using cerebellum opening book: https://zipproth.de/Brainfish/download/
	try:
		best_move = chess.polyglot.MemoryMappedReader("opening_book/cerebellum.bin").weighted_choice(board).move().uci()
		return format_response(best_move)
	except:
		best_move = engine(board, depth, player, null_move)
	
	end = time.time()
	print((end - st) * 1000)
	return format_response(best_move)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)
	mp.set_start_method("chess")
