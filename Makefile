SHELL=/bin/bash

help:
	@echo "simplified application building and running"
	@echo ""
	@echo " make fe      - build frontend part of the application"
	@echo " make be      - install backend dependencies"
	@echo " make db-init - initialize minimal database to run this application"
	@echo " make run-dev - run backend and frontend together for development"
	@echo ""
	@echo "Before run any of the option, please read README.md"

fe-kanban:
	@echo "Building vue.js kanban application"
	cd fe/kanban; npm install
	cd fe/kanban; npm run-script build

fe: fe-kanban
	@echo "Build of whole FE completed"



be:
	@echo "Installing dependencies for backend"
	cd app; pip3 install -r requirements.txt
	@echo ""
	@echo "Now you can run ./main.py under directory app, or run db-init if haven't done it yet"


db-init:
	@echo "Initialize new clear db"
	./db-init.py
	@echo ""


run-dev: be fe-kanban		# run prerequisities first
	@echo "Replace absolute devel app url and port"
	for f in `grep -l "localhost:5000" dist/`; do echo "Processing $f"; sed 's/http:\/\/localhost:5000//g' -i $f; done
	@echo "Deploy static to application bundle"
	rsync -avh fe/kanban/dist/ be/static/kanban/
	mv be/static/kanban/kanban.html.j2 be/templates/kanban.html.j2
	rm be/static/kanban/index.html
	@echo "Run whole app, FE will be served by Flask"
	cd api; ./main.py