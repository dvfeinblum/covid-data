from argparse import ArgumentParser
import csv
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import requests
from scipy.ndimage import gaussian_filter1d


class PlotBuilder:
    def __init__(self):
        self.run_date = datetime.now()
        self.data = {}
        self.data_rolling = {}
        self.region_list = ["nationwide", "northeast", "west", "south"]
        self.fig = plt.figure()

    def parse_row(self, row):
        """
        Chop csv row up across regions and store as (datetime, float) pairs
        """
        region = row["display_name"].lower()
        region_data = self.data.get(region, [])
        region_data.append(
            (
                datetime.strptime(row["date"], "%Y-%m-%d").date(),
                float(row["eff_conc_sarscov2_weekly"]),
            )
        )
        self.data[region] = region_data

        region_data_rolling = self.data_rolling.get(region, [])
        region_data_rolling.append(
            (
                datetime.strptime(row["date"], "%Y-%m-%d").date(),
                float(row["eff_conc_sarscov2_weekly_rolling"]),
            )
        )
        self.data_rolling[region] = region_data_rolling

    def plot(self, args):
        """
        For now, print the data either directly or smoothed.
        """
        region = args.region
        smooth = args.smooth
        rolling = args.rolling
        axes = self.fig.add_subplot()
        if not region:
            # reverse order so nationwide is on top
            for reg in self.region_list[::-1]:
                if rolling:
                    x, y = zip(*self.data_rolling[reg])
                else:
                    x, y = zip(*self.data[reg])
                    if smooth:
                        y = gaussian_filter1d(y, sigma=2)
                if reg == "nationwide":
                    axes.plot(x, y, label=reg, c="black", linewidth=2)
                else:
                    axes.plot(x, y, label=reg)

        else:
            if rolling:
                x, y = zip(*self.data_rolling[region])
            else:
                x, y = zip(*self.data[region])
                if smooth:
                    y = gaussian_filter1d(y, sigma=2)
            axes.plot(x, y, label=region)
        plt.legend(loc="upper left")
        plt.show()


def fetch_latest_data():
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


def parse_csv() -> PlotBuilder:
    """
    Parses Biobot csv and instantiates PlotBuilder object for
    plot building.
    """
    fetch_latest_data()
    with open("biobot/wastewater_by_census_region_nationwide.csv") as f:
        """
        Rows are of the form
        {
            'date': '2020-03-18',
            'display_name': 'Nationwide',
            'eff_conc_sarscov2_weekly': '99.58647478625',
            'eff_conc_sarscov2_weekly_rolling': '158.9905916924097'
        }
        """
        plot_builder = PlotBuilder()
        for row in csv.DictReader(f):
            plot_builder.parse_row(row)

    return plot_builder


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--region")
    parser.add_argument("--smooth", type=bool)
    parser.add_argument("--rolling", type=bool)
    args = parser.parse_args()

    plot_builder = parse_csv()
    plot_builder.plot(args)
