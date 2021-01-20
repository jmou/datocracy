ASSETS = cases-big.svg cases-small.svg deaths-big.svg deaths-small.svg \
	 tableau.json

all: $(ASSETS)

cases-big.svg: ../systrom/cases.bystate/big.svg
cases-small.svg: ../systrom/cases.bystate/small.svg
deaths-big.svg: ../systrom/deaths.bystate/big.svg
deaths-small.svg: ../systrom/deaths.bystate/small.svg

tableau.json: ../nyvaccine/tableau.json

$(ASSETS):
	cp $< $@
