# version: 1.0.0
.PHONY: all unittest integrationtest test integrationtest_manual integrationtest_auto coverage

all: test

test: unittest integrationtest

unittest:
	@"$(MAKE)" -C unittest test

integrationtest: integrationtest_auto integrationtest_manual

integrationtest_auto:
	@"$(MAKE)" -C integrationtest_auto test

integrationtest_manual:
	@"$(MAKE)" -C integrationtest_manual test

coverage:
	@"$(MAKE)" -C integrationtest_auto coverage
	@"$(MAKE)" -C unittest coverage
	@"$(MAKE)" -C unittest combine_coverage
