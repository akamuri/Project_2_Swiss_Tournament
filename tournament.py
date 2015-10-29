#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import time


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches;")
    DB.commit()
    DB.close ()
"""Remove all the match records from the database."""


def deletePlayers():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM Players;")
    DB.commit()
    DB.close ()
"""Remove all the player records from the database."""


def countPlayers():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM Players;")
    countPy = c.fetchone()[0]
    DB.close ()
    return countPy
"""Returns the number of players currently registered."""


def registerPlayer(name):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO Players (name) VALUES (%s)",(bleach.clean(name),))
    DB.commit()
    DB.close()
"""Adds a player to the tournament database.

The database assigns a unique serial id number for the player.  (This
should be handled by your SQL database schema, not in your Python code.)

Args:
  name: the player's full name (need not be unique).
"""


def playerStandings():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT player_id, name, player_wins, player_matches FROM Players ORDER BY player_wins DESC")
    standings = [(int(row[0]), str(row[1]), int(row[2]),int(row[3])) 
            for row in c.fetchall()]
    DB.close ()
    return standings


    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    DB = connect()
    c = DB.cursor()
    c.execute("UPDATE Players SET player_wins = player_wins + 1 WHERE player_id = (%s)",(winner,))
    c.execute("UPDATE Players SET player_matches = player_matches + 1 WHERE player_id = (%s) OR player_id = (%s)",(winner,loser,))
    c.execute("INSERT INTO Matches VALUES (DEFAULT, (%s) ,(%s))",(winner,loser,))
    DB.commit()
    DB.close()
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """


def swissPairings():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT player_id, name FROM Players ORDER BY player_wins DESC")
    rowfetch = c.fetchall()
    pairings =[]
    for i in range(0,(len(rowfetch)-1),2):
        if rowfetch[i+1]:
            pairings.append(rowfetch[i]+rowfetch[i+1])

    DB.close ()
    return pairings

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


