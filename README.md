Tournament Planner
==================

This python project organizes a tournament following the Swiss system.
Players and matches can be registered and deleted into/from a database,
and match pairings for the next round are decided based on previous matches.

To setup the system, create a postgresql database called tournament 
and execute the tournament.sql script to create the necessary tables and views.

File tournament.py contains all functions necessary to fulfill
the functionalities described.

Finally, to execute some tests, run:
python tournament_test.py
