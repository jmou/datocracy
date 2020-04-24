docs: www
	cp -R www docs
	rm -f docs/Makefile docs/.gitignore

www: systrom
	$(MAKE) -C www

systrom:
	$(MAKE) -C systrom

.PHONY: www systrom
