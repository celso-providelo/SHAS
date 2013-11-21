# Makefile for SHAS project
#

PYTHON=python

clean:
	@echo "Cleanup workspace"
	@rm -f */*.pyc

run-gunicorn:
	@echo "Running Flask app via Gunicorn"
	gunicorn -k flask_sockets.worker shas:app -t 3

run-public:
	@echo "Running Flask app via Gunicorn publicly"
	gunicorn -k flask_sockets.worker shas:app -t 3 -b 0.0.0.0

run:
	@echo "Running Flask app via Gevent"
	$(PYTHON) shas.py
