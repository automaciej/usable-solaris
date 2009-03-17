# vim: ft=make ts=4 sw=4 noet

default:
	@echo "You are in the pkg/ directory."

%:
	$(MAKE) -C trunk $* 

paranoid-%:
	$(MAKE) -C trunk $* || exit 2 

export BUILDLOG ?= $(shell pwd)/buildlog.txt

report-%:
	$(MAKE) -C trunk $* || echo "	*** make $* in $$i failed ***" >> $(BUILDLOG) 
