.PHONY: bump
bump:
	bump2version $(filter-out $@,$(MAKECMDGOALS))
	@git --no-pager show HEAD
	@echo
	@git verify-commit HEAD
	@git verify-tag `git describe`
	@echo
	# git push origin master --tags
%:
	@:
