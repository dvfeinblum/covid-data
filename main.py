import constants as c
from utils.parsers import build_arg_parser, parse_biobot, parse_cdc, parse_verily

if __name__ == "__main__":
    parser = build_arg_parser()
    args = parser.parse_args()
    if args.dimension == c.HOSPITALIZATIONS:
        plot_builder = parse_cdc(args)
    elif args.dimension == c.VERILY:
        plot_builder = parse_verily(args)
    else:
        plot_builder = parse_biobot(args)
    plot_builder.plot()
