#!/usr/bin/env python
#
# tournament_init.py -- database initialization
#
import tournament


def databaseInit():
    """
    Initialize database tournament as defined in tournament.sql
    """
    with tournament.connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(open("tournament.sql", "r").read())

# initialize tournament db as defined in tournment.sql
databaseInit()
