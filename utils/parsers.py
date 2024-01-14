from argparse import ArgumentParser
import csv

from constants import DIMENSIONS, REGIONS, TIMESCALES
from plot_builder import (
    BiobotPlotBuilder,
    CDCHospitalizationsPlotBuilder,
    VerilyWastewaterPlotBuilder,
)
from utils.data_proc import fetch_latest_biobot_data


def parse_biobot(args: ArgumentParser) -> BiobotPlotBuilder:
    """
    Parses Biobot csv and instantiates BiobotPlotBuilder object for
    plot building.
    """
    fetch_latest_biobot_data()
    with open("biobot/wastewater_by_census_region_nationwide.csv") as f:
        plot_builder = BiobotPlotBuilder(args)
        for row in csv.DictReader(f):
            plot_builder.parse_row(row)

    return plot_builder


def parse_cdc(args: ArgumentParser) -> CDCHospitalizationsPlotBuilder:
    with open("cdc/weekly_hospitalizations.csv") as f:
        plot_builder = CDCHospitalizationsPlotBuilder(args)
        for row in csv.DictReader(f):
            # temporary
            if row["State"] == "COVID-NET":
                plot_builder.parse_row(row)

    return plot_builder


def parse_verily(args: ArgumentParser) -> VerilyWastewaterPlotBuilder:
    with open("wastewaterscan/condensed.csv") as f:
        plot_builder = VerilyWastewaterPlotBuilder(args)
        for row in csv.DictReader(f):
            plot_builder.parse_row(row)

    return plot_builder


def build_arg_parser():
    parser = ArgumentParser()
    parser.add_argument("--region", required=False, type=str, choices=REGIONS)
    parser.add_argument("--smooth", action="store_true", required=False)
    parser.add_argument("--rolling", action="store_true", required=False)
    parser.add_argument("--timescale", required=False, type=str, choices=TIMESCALES)
    parser.add_argument("--dimension", type=str, choices=DIMENSIONS)

    return parser
