from csv import DictReader, DictWriter
from datetime import datetime
from functools import reduce

import requests


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


def nationalize_wastewater_scan():
    """
    wastewater scan data is a mess and is per site. rows are of the form
    ['\ufeff"sample_id"',
    "collection_date",
    "bcov_recovery",
    "bcov_recovery_lci",
    "bcov_recovery_uci",
    "city",
    "state",
    "name",
    "site_name",
    "sewershed_pop",
    "state_abbr",
    "N_Gene_gc_g_dry_weight",
    'N_Gene_gc_g_dry_weight_lci',
    'N_Gene_gc_g_dry_weight_uci']
    """
    simplified_data = {}
    with open("wastewaterscan/WWSCAN_SARSCoV2_All_Wastewater_Sites_20240113.csv") as f:
        for row in DictReader(f):
            date_str = row["collection_date"]
            date_set = simplified_data.get(date_str, [])
            date_set.append(float(row["N_Gene_gc_g_dry_weight"]))
            simplified_data[date_str] = date_set

    avg_per_day = []
    for k, v in simplified_data.items():
        avg_per_day.append(
            {"date": k, "avg_amt": reduce(lambda x, y: x + y, v) / len(v)}
        )

    with open("wastewaterscan/condensed.csv", "w") as g:
        writer = DictWriter(g, fieldnames=list(avg_per_day[0].keys()))
        writer.writeheader()
        writer.writerows(avg_per_day)
