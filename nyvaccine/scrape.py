# flake8: noqa
# https://stackoverflow.com/a/64179945/13773246

import html
import json
import re
import sys
from urllib.parse import urlencode
from urllib.request import urlopen

# embedded in https://covid19vaccine.health.ny.gov/covid-19-vaccine-tracker
url = 'https://covid19tracker.health.ny.gov/views/Vaccine_Management_public/NYSVaccinations?:embed=y&:showVizHome=n&:tabs=n&:toolbar=n&:device=desktop&:apiID=host0#navType=1&navSrc=Parse'
with urlopen(url) as fh:
    match = re.search(rb'<textarea id="tsConfigContainer">(.*?)</textarea>', fh.read())
config = json.loads(html.unescape(match[1].decode('ascii')))

url = f"https://covid19tracker.health.ny.gov{config['vizql_root']}/bootstrapSession/sessions/{config['sessionid']}"
with urlopen(url, urlencode({'sheet_id': config['sheetId']}).encode('ascii')) as fh:
    raw = fh.read().decode('utf-8')

match = re.fullmatch(r'\d+;({.*})\d+;({.*})', raw)
info = json.loads(match[1])
data = json.loads(match[2])

json.dump(data, sys.stdout, sort_keys=True, indent=4)
print()
# print(data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"])
