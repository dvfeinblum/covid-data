YEAR = "year"
SIX_MONTHS = "six_months"

HOSPITALIZATIONS = "hospitalizations"
WASTEWATER = "wastewater"
VERILY = "verily"

TIMESCALES = [YEAR, SIX_MONTHS]
DIMENSIONS = [HOSPITALIZATIONS, WASTEWATER, VERILY]

NATIONWIDE = "nationwide"
NORTHEAST = "northeast"
MIDWEST = "midwest"
WEST = "west"
SOUTH = "south"
REGIONS = [NATIONWIDE, NORTHEAST, MIDWEST, WEST, SOUTH]

# note: this mapping is based on biobot's definitions
STATE_TO_REGION_DICT = {
    "utah": WEST,
    "new mexico": WEST,
    "oregon": WEST,
    "california": WEST,
    "connecticut": NORTHEAST,
    "new york": NORTHEAST,
    "ohio": MIDWEST,
    "minnesota": MIDWEST,
    "michigan": MIDWEST,
    "georgia": SOUTH,
    "iowa": MIDWEST,
    "maryland": NORTHEAST,
    "tennessee": SOUTH,
    "covid-net": NATIONWIDE,
    "colorado": WEST,
}
