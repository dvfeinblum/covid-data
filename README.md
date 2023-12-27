# covid-data
playin around with covid stats


# how to use
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python main.py --dimenions hospitalizations
```

the script has a few flags you can play with:

* `--region` allows you to only plot a specific region. options are `["nationwide", "northeast", "west", "south"]`
* `--smooth` applies a gaussian filter to the data with a sigma of 2
* `--rolling` switches from the absolute data on each date to a rolling avg that is calculated by biobot themselves
* `--timescale` only shows a select portion of the data. options are `["year", "six_months"]`
* `--dimension` selects which data you want to view. opetions are `["hospitalizations", "wastewater"]`. note that the former is from the cdc and the latter is from biobot

you can mix and match these however you like.
