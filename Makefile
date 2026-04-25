all: localecompile
LNGS:=`find pretalx_sso/locale/ -mindepth 1 -maxdepth 1 -type d -printf "-l %f "`

localecompile:
	django-admin compilemessages

localegen:
	django-admin makemessages -l de_DE -i build -i dist -i "*egg*" $(LNGS)

style:
	isort .
	flake8 .
	black .
	find -name "*.html" | xargs djhtml
	check-manifest .
	python -m build
	twine check dist/*

.PHONY: all localecompile localegen style
