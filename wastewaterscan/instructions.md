this data set is massive (like 18 mb) and it feels silly checking it into git
to get this data the process is a little circuitous:
1. go to https://data.wastewaterscan.org/ and select all sites
1. click the folder and select download only targest and plants on this chart
1. this'll give ya all the covid data they have and we expect a filename of the form `WWSCAN_SARSCoV2_All_Wastewater_Sites_YYYYMMDD.csv`
1. Then for now, manually run `utils.data_proc.nationalize_wastewater_scan`
