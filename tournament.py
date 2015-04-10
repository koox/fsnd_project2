#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("delete from matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("delete from players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("select count(*) from players")
    count = cur.fetchall()[0][0]
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("insert into players (name) values (%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("select * from player_standings")
    rows = cur.fetchall()
    conn.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("insert into matches (winner)"
                "values (%s) RETURNING id", (winner,))
    match_id = cur.fetchone()[0]
    cur.execute("insert into players_to_matches (player_id,match_id)"
                "values (%s,%s)", (winner, match_id,))
    cur.execute("insert into players_to_matches (player_id,match_id)"
                "values (%s,%s)", (loser, match_id,))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # get the players ordered by # of wins
    players = playerStandings()
    pairs = []
    # check if players are odd numbered
    if countPlayers() % 2:
        # returns the id of a random player who have had no bye round yet
        odd_player_id = oddPlayer()
        # find the player who will have the bye round in the list
        # and place him at the end of the list
        odd_player_idx = [item for item, v in enumerate(players)
                          if v[0] == odd_player_id[0]]
        players.append(players.pop(odd_player_idx[0]))
        # and make the players even again by appending an empty player
        players.append((None, None, None, None))
    # create the pairs
    for i in range(0, len(players) - 1, 2):
        pairs.append((players[i][0],
                      players[i][1],
                      players[i+1][0],
                      players[i+1][1]))
    return pairs


def oddPlayer():
    """Return the id of a random player who have had no bye round yet"""
    conn = connect()
    cur = conn.cursor()
    #  not select the ones that have an odd number off opponents
    #  and orde by random
    cur.execute("select p.id from players as p where "
                "p.id NOT IN "
                "(select pm.player_id , count(pm.player_id) as num "
                "from players_to_matches as pm "
                "group by pm.match_id "
                "having mod(num,2) = 1) "
                "order by random()")
    player_id = cur.fetchone()
    conn.close()
    if player_id:
        return player_id
    else:
        return False
