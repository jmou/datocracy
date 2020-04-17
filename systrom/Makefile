# http://systrom.com/covid19-charts-us-states/
# Says the page will be updated daily, but hasn't been updated in 2 weeks.
#
# Introduced in http://systrom.com/blog/the-us-just-crossed-a-dangerous-threshold/
# Article written at a point in time but now difficult to reproduce with evolved
# data sets.

# https://en.wikipedia.org/wiki/Special:ApiSandbox
scrape.json:
	curl -fso $@ 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=Template%3A2019%E2%80%9320%20coronavirus%20pandemic%20data%2FUnited%20States%20medical%20cases&formatversion=2&rvprop=ids%7Ctimestamp%7Ccontent&rvslots=main'

scrape.wikitext: scrape.json
	python3 -c "import json, sys; print(json.load(sys.stdin)['query']['pages'][0]['revisions'][0]['slots']['main']['content'])" < $< > $@

venv:
	python3 -m venv $@

requirements.txt:
	./venv/bin/pip install wikitextparser matplotlib
	./venv/bin/pip freeze > $@

cases.csv deaths.csv &: scrape.wikitext parse.py
	./venv/bin/python3 parse.py cases.csv deaths.csv < $<
