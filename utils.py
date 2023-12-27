from argparse import ArgumentParser
import csv
from datetime import datetime

import requests

from constants import DIMENSIONS, REGIONS, TIMESCALES
from plot_builder import BiobotPlotBuilder, CDCHospitalizationsPlotBuilder


def fetch_latest_biobot_data():
    """
    Biobot uploads new data on mondays. We check the lock file
    to see when we last fetched data. If it's tuesday, try fetching
    the latest data.

    Raises HTTPError if we attempt to refresh and fail for some reason.
    """
    today = datetime.today()

    # only bother looking for new data on tuesday
    if today.weekday() == 0:
        file_date = today.strftime("%Y-%m-%d")
        # use a+ so we don't overwrite but get a new file if the lock DNE
        with open("biobot/.biobot.lock", "a+") as f:
            # seek first since, if file exists, we'll be at the end
            f.seek(0)
            last_updated = f.read().strip()
            if last_updated != file_date:
                print("biobot data is stale; fetching new data.")
                file_url = f"https://d1t7q96h7r5kqm.cloudfront.net/{file_date}_automated_csvs/wastewater_by_census_region_nationwide.csv"
                with open(
                    "biobot/wastewater_by_census_region_nationwide.csv", "w"
                ) as g:
                    resp = requests.get(file_url)
                    resp.raise_for_status()
                    for line in resp.iter_lines():
                        str_line = line.decode("utf-8")
                        if "#" in str_line:
                            # for some reason, they prepend data w/comment row
                            continue
                        else:
                            g.write(str_line + "\n")

                # update last_updated datestring in lock file
                f.seek(0)
                f.truncate()
                f.write(file_date)


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


def build_arg_parser():
    parser = ArgumentParser()
    parser.add_argument("--region", required=False, type=str, choices=REGIONS)
    parser.add_argument("--smooth", action="store_true", required=False)
    parser.add_argument("--rolling", action="store_true", required=False)
    parser.add_argument("--timescale", required=False, type=str, choices=TIMESCALES)
    parser.add_argument("--dimension", type=str, choices=DIMENSIONS)

    return parser
