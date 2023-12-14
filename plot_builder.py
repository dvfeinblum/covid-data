from datetime import datetime

from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

from constants import YEAR, SIX_MONTHS, REGIONS


class PlotBuilder:
    def __init__(self, args):
        self.data = {}
        self.data_rolling = {}
        self.fig = plt.figure()
        self.args = args
        self.run_date = datetime.today().date()

    def parse_row(self, row):
        """
        Chop csv row up across regions and store as (datetime, float) pairs
        """
        region = row["display_name"].lower()
        region_data = self.data.get(region, [])
        row_date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        if self.args.timescale == YEAR:
            if row_date < self.run_date - relativedelta(years=1):
                return
        if self.args.timescale == SIX_MONTHS:
            if row_date < self.run_date - relativedelta(months=6):
                return

        region_data.append(
            (
                row_date,
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

    def plot(self):
        """
        For now, print the data either directly or smoothed.
        """
        region = self.args.region
        smooth = self.args.smooth
        rolling = self.args.rolling
        axes = self.fig.add_subplot()
        if not region:
            # reverse order so nationwide is on top
            for reg in REGIONS[::-1]:
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
        plt.legend(loc="upper right")
        plt.show()
