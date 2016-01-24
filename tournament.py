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
    c = conn.cursor()
    c.execute("delete from matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) from players;")
    count = c.fetchone()[0]
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
    c = conn.cursor()
    c.execute("insert into players (name) values (%s);", (name,))
    conn.commit()
    conn.close()


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
    """
    conn = connect()
    c = conn.cursor()
    # summary is a view that returns exactly the info described in the docstring
    c.execute("select id, name, wins, matches from summary;")
    results = c.fetchall()
    conn.close()
    return results



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into matches (winner_id, loser_id) values (%s, %s);", (winner, loser))
    conn.commit()
    conn.close()

def checkMatch(winner,loser):
    """Checks if a match already exists in db.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost

    Returns:
      True if match happened, False otherwise
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select id from matches where winner_id = %s and loser_id = %s;", 
        (winner, loser))
    # if there is at least one row returned, match happened
    for row in c.fetchall():
        return True
    return False
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Avoiding repeating matches:
    We will start with the current first place, and check from the second onwards
    until finding the first one where the match did not happen yet, creating it.
    This goes on for each next player. If in the end this iteration there are 
    still players unmatched, they will be paired, regardless if match already happened.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    results = []
    # create a dictionary with players that still need to be matched
    # keys are ids, values are names
    players_to_be_matched = dict([(player[0], player[1]) for player in standings])
    index = 0
    for player in standings:
        if player[0] not in players_to_be_matched:
            # player already matched, check next one
            index+=1
            continue
        for oponent in standings[index+1:]:
            if oponent[0] not in players_to_be_matched:
                # oponent already matched, check next one
                continue
            if checkMatch(player[0], oponent[0]):
                # match already happened, check next one
                continue
            results.append((player[0], player[1], oponent[0], oponent[1]))
            players_to_be_matched.pop(player[0], None) 
            players_to_be_matched.pop(oponent[0], None)
            break
        index+=1

    # if there are any players left, match them sequentially
    first_player = True
    for player_id, player_name in players_to_be_matched.items():
        if first_player:
            id = player_id
            name = player_name
            first_player = False
            continue
        results.append((id, name, player_id, player_name))
        first_player = True
    return results
