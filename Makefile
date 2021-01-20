docs: www
	cp -R www docs
	rm -f docs/Makefile docs/.gitignore

www: nyvaccine systrom
	$(MAKE) -C www

nyvaccine systrom:
	$(MAKE) -C $@

.PHONY: www nyvaccine systrom
