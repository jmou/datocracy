SVGS = cases-big.svg cases-small.svg deaths-big.svg deaths-small.svg

all: $(SVGS)

cases-big.svg: ../systrom/cases.bystate/big.svg
cases-small.svg: ../systrom/cases.bystate/small.svg
deaths-big.svg: ../systrom/deaths.bystate/big.svg
deaths-small.svg: ../systrom/deaths.bystate/small.svg

$(SVGS):
	cp $< $@
