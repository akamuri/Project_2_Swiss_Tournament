#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database.
    Used cursor() to execute SQL command to DELETE all data from the matches table.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches;")
    DB.commit()
    DB.close ()



def deletePlayers():
    """Remove all the player records from the database.
    Used cursor() to execute SQL command to DELETE all data from the Players table.
    """    
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM Players;")
    DB.commit()
    DB.close ()



def countPlayers():
    """Returns the number of players currently registered.
    Executed SQL command to COUNT all rows from the Players table.
    Then Used c.fetchone()[0] to obtain the count value and return it.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM Players;")
    countPy = c.fetchone()[0]
    DB.close ()
    return countPy



def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args: 
    name: the player's full name (need not be unique).
    
    Executed INSERT into players table, %s allows the Query to understand 'name'.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO Players (name) VALUES (%s)",(name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played

    Used c.fetchall the results of the SQL Query are converted to a list of tuples and the is returned.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT player_id, name, player_wins, player_matches FROM Players ORDER BY player_wins DESC")
    standings = [(int(row[0]), str(row[1]), int(row[2]),int(row[3])) 
            for row in c.fetchall()]
    DB.close ()
    return standings


def reportMatch(winner, loser):    
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost

    The SQL Query UPDATE the 'Players' and 'Matches' tables with winner and loser infromation.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("UPDATE Players SET player_wins = player_wins + 1 WHERE player_id = (%s)",(winner,))
    c.execute("UPDATE Players SET player_matches = player_matches + 1 WHERE player_id = (%s) OR player_id = (%s)",(winner,loser,))
    c.execute("INSERT INTO Matches VALUES (DEFAULT, (%s) ,(%s))",(winner,loser,))
    DB.commit()
    DB.close()


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

    Used a for loop the increments by 2 the list of standings can be converted into a list of pairings.
    rowfetch[i]+rowfetch[i+1] allows the for loop to look at 2 playerIDs at the same time and add them to the tuple.
    """
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


