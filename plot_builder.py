from abc import ABC, abstractmethod
from datetime import datetime

from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from scipy.ndimage import gaussian_filter1d

from constants import NATIONWIDE, REGIONS, SIX_MONTHS, YEAR


class PlotBuilder(ABC):
    def __init__(self, args):
        self.data = {}
        self.data_rolling = {}
        self.fig = plt.figure()
        self.args = args
        self.run_date = datetime.today().date()

    @abstractmethod
    def parse_row(self, row: str):
        pass

    @abstractmethod
    def produce_data(self):
        pass

    def plot(self):
        axes = self.fig.add_subplot()
        self.produce_data(axes)
        plt.legend(loc="upper right")
        plt.show()


class BiobotPlotBuilder(PlotBuilder):
    def produce_data(self, axes: Axes):
        region = self.args.region
        smooth = self.args.smooth
        rolling = self.args.rolling
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

    def parse_row(self, row: str):
        """
        Rows are of the form
        {
            'date': '2020-03-18',
            'display_name': 'Nationwide',
            'eff_conc_sarscov2_weekly': '99.58647478625',
            'eff_conc_sarscov2_weekly_rolling': '158.9905916924097'
        }
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


class CDCHospitalizationsPlotBuilder(PlotBuilder):
    def parse_row(self, row: str):
        """
        Rows are of the form:
        {
            'State': 'New Mexico',
            'Season': '2019-20',
            'Week ending date': '03/28/2020 12:00:00 AM',
            'Age Category': '0-4 years',
            'Sex': 'All',
            'Race': 'All',
            'Rate': '0',
            'Cumulative Rate': '0'}
        """
        region_data = self.data.get(NATIONWIDE, [])
        region_data.append(
            (
                datetime.strptime(
                    row["Week ending date"], "%m/%d/%Y %H:%M:%S %p"
                ).date(),
                float(row["Rate"]),
            )
        )
        self.data[NATIONWIDE] = region_data

    def produce_data(self, axes: Axes):
        x, y = zip(*self.data[NATIONWIDE])
        axes.bar(x, y, label=NATIONWIDE, width=7)
