
import click
import multiprocessing

from config import Config
from typing import Optional

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
    # default="alpha_beta"
    default="iterative_deepening"
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
@click.option(
    "--syzygy-pieces",
    type=int,
    help="Remaining pieces to use syzygy endgame tablebases.",
    default=5
)
def main(
    mode: str,
    algorithm: str,
    depth: int,
    null_move: bool,
    null_move_r: int,
    quiescence_search_depth: int,
    syzygy_path: Optional[str],
    syzygy_pieces: int,
):
    """
    Starts the engine according to the options provided.
    """
    config = Config(
        mode=mode,
        algorithm=algorithm,
        negamax_depth=depth,
        null_move=null_move,
        null_move_r=null_move_r,
        quiescence_search_depth=quiescence_search_depth,
        syzygy_path=syzygy_path,
        syzygy_pieces=syzygy_pieces,
    )
    run(config)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
