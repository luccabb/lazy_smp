
import click
import multiprocessing

from config import Config
from typing import Optional
import chess.syzygy

from mode.uci import main as uci_main
from mode.api import main as api_main


def run(config: Config):
    if config.mode == "uci":
        uci_main(config)
    elif config.mode == "api":
        api_main()
    else:
        raise ValueError("mode not supported, type --help to see supported modes.")


@click.command()
@click.option(
    "--mode",
    type=str,
    help="Mode to run the engine, one of [uci, api].",
    default="uci"
)
@click.option(
    "--algorithm",
    type=str,
    help="Algorithm to use to search move.",
    default="alpha_beta"
)
@click.option(
    "--depth",
    "--negamax-depth",
    type=int,
    help="Depth of negamax search.",
    default=4
)
@click.option(
    "--null-move",
    type=bool,
    help="If True, use null move prunning.",
    default=False,
)
@click.option(
    "--null-move-r",
    type=int,
    help="Null move reduction factor.",
    default=2,
)
@click.option(
    "--quiescence-search-depth",
    type=int,
    help="Max depth of quiescence search.",
    default=3
)
@click.option(
    "--syzygy-path",
    type=str,
    help="Path to syzygy endgame tablebases.",
    default=None
)
def main(
    mode: str,
    algorithm: str,
    depth: int,
    null_move: bool,
    null_move_r: int,
    quiescence_search_depth: int,
    syzygy_path: Optional[str]
):
    """
    Starts the engine according to the options provided.
    """
    if syzygy_path:
        tablebase = chess.syzygy.open_tablebase(syzygy_path)
    else:
        tablebase = None
    
    config = Config(
        mode=mode,
        algorithm=algorithm,
        negamax_depth=depth,
        null_move=null_move,
        null_move_r=null_move_r,
        quiescence_search_depth=quiescence_search_depth,
        tablebase=tablebase,
    )
    run(config)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
