# http://systrom.com/covid19-charts-us-states/
# Says the page will be updated daily, but hasn't been updated in 2 weeks.
#
# Introduced in http://systrom.com/blog/the-us-just-crossed-a-dangerous-threshold/
# Article written at a point in time but now difficult to reproduce with evolved
# data sets.

SHELL = /bin/bash

all: cases.bystate/big.svg cases.bystate/small.svg deaths.bystate/big.svg deaths.bystate/small.svg

venv:
	python3 -m venv $@

venv/updated: venv
	./venv/bin/pip install -r requirements.txt
	touch $@

requirements.txt: venv
	./venv/bin/pip install wikitextparser numpy matplotlib
	./venv/bin/pip freeze > $@

# https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_coronavirus_pandemic_data/United_States_medical_cases
# https://en.wikipedia.org/wiki/Special:ApiSandbox
scrape.json:
	curl -fso scrape.json 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=Template%3A2019%E2%80%9320%20coronavirus%20pandemic%20data%2FUnited%20States%20medical%20cases&formatversion=2&rvprop=ids%7Ctimestamp%7Ccontent&rvslots=main'

scrape.wikitext: scrape.json
	python3 -c "import json, sys; print(json.load(sys.stdin)['query']['pages'][0]['revisions'][0]['slots']['main']['content'])" < $< > $@

# More properly this would use the new (make 4.3) grouped targets.
cases.csv deaths.csv: scrape.wikitext parse.py venv/updated
	./venv/bin/python3 parse.py cases.csv deaths.csv < $<

%.bystate: %.csv normalize_by_state.py venv/updated
	./venv/bin/python3 normalize_by_state.py $@ < $<

%.bystate/max.dsv: %.bystate
	awk -F, 'ENDFILE{print gensub(/.*\/(..)\.csv/,"\\1",1,FILENAME),$$2}' $</*.csv > $@

%.bystate/cutoff.value: %.bystate/max.dsv
	cut -d' ' -f2 < $< | sort -n | tail -n+20 | head -n1 > $@

%.bystate/big.states: %.bystate/max.dsv %.bystate/cutoff.value
	awk -v cutoff=$$(<$*.bystate/cutoff.value) '$$2>cutoff{print $$1}' $< > $@

%.bystate/small.states: %.bystate/max.dsv %.bystate/cutoff.value
	awk -v cutoff=$$(<$*.bystate/cutoff.value) '$$2<=cutoff{print $$1}' $< > $@

# This rule isn't able to express the dependency on %.bystate
%.svg: export TZ = America/New_York
%.svg: %.states graph.py scrape.json venv/updated
	sort $< | ./venv/bin/python3 graph.py $$(dirname $<) $$(grep -o ^[^.]* <<< $<) "$$(date -d @$$(stat -c %Y scrape.json) +'%Y-%m-%d %H:%M %Z')" $@

.SECONDARY:
