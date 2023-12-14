from utils import build_arg_parser, parse_csv

if __name__ == "__main__":
    parser = build_arg_parser()
    args = parser.parse_args()
    plot_builder = parse_csv(args)
    plot_builder.plot()
