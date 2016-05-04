#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM match")
    DB.commit()
    DB.close()

def deletePlayersInTournament():
    """Remove all the players in a tournament"""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM player_tournament")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM player")
    DB.commit()
    DB.close()

def deleteTounament():
    """Remove all torunaments records from the database"""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM tournament")
    DB.commit()
    DB.close()

def deleteMatchesInTournament(id_tournament):
    """Remove all the match records from the from an tournament
   
    Arg: 
    id_tournament: id number of the tournament
    """
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM match WHERE id_tournament = %s", (id_tournament, ))
    DB.commit()
    DB.close()

def countTournaments():
    """Returns the number of tournaments currently registered in the database. 
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(1) FROM tournament")
    tournament = c.fetchone()[0]
    DB.close()
    return tournament

def countPlayers(id_tournament):
    """Returns the number of players currently registered for a tournament.
        Args:
        id_tournament: the id of the tournament
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(1) FROM player_tournament WHERE id_tournament = %s",(id_tournament,))
    players = c.fetchone()[0]
    DB.close()
    return players

def registerTournament(name):
    """Adds a tournament to the tournament database.

    Returns:
        The id number of the tournament
    """
    name = bleach.clean(name)
    DB = connect()
    c = DB.cursor()
    c.execute("insert into tournament (name) values (%s) RETURNING id", (name,))
    DB.commit()
    tournamentid = c.fetchone()[0]
    DB.close()
    return tournamentid

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).

    Returns:
      the id of Player that is registered
    """
    name = bleach.clean(name)
    DB = connect()
    c = DB.cursor()
    c.execute("insert into player (name) values (%s) RETURNING id", (name,))
    DB.commit()
    playerid = c.fetchone()[0]
    DB.close()
    return playerid

def registerPlayerInTournament(id_tournament, id_player):
    """Adds a player into an specific tournamen.

    Args:
        id_tournament: the id of the tournament
        id_player: the if of the player
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into player_tournament (id_tournament, id_player) values (%s, %s)", (id_tournament,id_player,))
    DB.commit()
    DB.close()

def playerStandings(id_tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args: 
        id_tournament: id of tournament getting standings for
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the numb  er of matches the player has won
        matches: the number of matches the player has played
        id_player_tournament: the id of relation between player and tournament
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT id, name, wins, wins+loses as matches, id_player_tournament FROM scoreboard WHERE id_tournament = (%s) ORDER BY wins DESC",(id_tournament,))
    standings = []
    for row in c.fetchall():
        standings.append(row)
    DB.close()
    return standings

def reportMatch(winner, loser, id_tournament):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player_tournament of the player who won
      loser:  the id number of the player_tournament of the player who lost
      id_tournament: the id number of the tournament
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into match (winner, loser, id_tournament) values (%s, %s, %s)", (winner,loser,id_tournament,))
    DB.commit()
    DB.close()
 
def checkByes(id_tournament, standings, index):
    """Check if the players already have a bye
    
    Arg:
    id_tournament: id number of the torunament
    standings: list of the current ranks
    index: the index to check if have a bye
    """
    if abs(index) > len(standings):
        return -1
    elif hasBye(standings[index][4], id_tournament):
        return index
    else:
        return checkByes(id_tournament, standings, (index -1))

def hasBye(id_player_tournament, id_tournament):
    """Check if the players in a tournament has a bye

    Arg:
    id_player_tournament: id number of the player in a tournament
    id_tournament: id number of the tournament

    Return:
    False if already have a Bye otherwise True
    """
    DB = connect()
    c= DB.cursor()
    c.execute("SELECT count(1) FROM match WHERE id_tournament = %s AND winner = %s and loser IS NULL",
             (id_tournament,id_player_tournament))
    bye = c.fetchone()[0]
    DB.close()
    if bye == 0:
        return True
    else:
        return False

def checkPairs(id_tournament, standings, id1, id2):
    """Checks if two players have already had a match against each other.
    If they have, going to checks through the list until a valid match is
    found.
    Args:
        id_tournament: id number of the tournament
        standings: list of current ranks from swissPairings()
        id1: id position of player into the standings needing a match
        id2: id position of player into the standings that is potential matched player
    Returns id of matched player or original match if none are found.
    """
    if id2 >= len(standings):
        return id1 + 1
    elif validPair(standings[id1][4], standings[id2][4], id_tournament):
        return id2
    else:
        return checkPairs(id_tournament, standings, id1, (id2 + 1)) 

def validPair(player1, player2, id_tournament):
    """Checks if two players have already played against each other
    Args:
        player1: the id number of first player id into the tournament to check
        player2: the id number of potentail paired player id into the tournament
        id_tournament: the id number of the tournament
    Return true if valid pair, false if not
    """
    DB = connect()
    c = DB.cursor()
    c.execute("""SELECT COUNT(1) 
                FROM match 
                WHERE ((winner = %s AND LOSER = %s) 
                    OR (winner = %s AND LOSER = %s))
                AND id_tournament = %s
                """, (player1, player2, player2, player1, id_tournament))
    find = c.fetchone()[0]
    DB.close()
    if find > 0:
        return False
    return True

def swissPairings(id_tournament):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    
    Arg:
    id_tournament: id number of the tournament
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings(id_tournament)
    numPlayers = countPlayers(id_tournament)
    pairs = []
    if numPlayers % 2 != 0:
        bye = standings.pop(checkByes(id_tournament, standings, -1))
        reportMatch(bye[4], None, id_tournament)
    
    while len(standings) > 1:
        validMatch = checkPairs(id_tournament,standings,0,1)
        player1 = standings.pop(0)
        player2 = standings.pop(validMatch-1)
        pairs.append((player1[0],player1[1],player2[0],player2[1]))
    return pairs

