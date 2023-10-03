legume:
	cd src; python3 legume.py

delete_db:
	rm -f src/data/db.sqlite3*
	rm -f src/data/tmp/*
