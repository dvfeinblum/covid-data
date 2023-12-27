from constants import HOSPITALIZATIONS
from utils import build_arg_parser, parse_biobot, parse_cdc

if __name__ == "__main__":
    parser = build_arg_parser()
    args = parser.parse_args()
    if args.dimension == HOSPITALIZATIONS:
        plot_builder = parse_cdc(args)
    else:
        plot_builder = parse_biobot(args)
    plot_builder.plot()
