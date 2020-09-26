SHELL := /bin/bash
.ONESHELL:
default:
	source django/bin/activate
	cd django/busnav/
	python3 manage.py runserver
