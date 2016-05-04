#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from tournament import *

def tesDetele():
    """
    Test for delete all the information in database
        and there is no tournmanets registered
    """
    deleteMatches()
    deletePlayersInTournament()
    deletePlayers()
    deleteTounament()
    c = countTournaments()
    if c == '0':
        raise TypeError(
            "countTournaments should return numeric zero, not string '0'")
    if c != 0:
        raise TypeError(
            "After deletion, countTournaments should return zero.")    
    print "1 . deleted all information from database"

def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    id_tournament = registerTournament('test 1')
    c = countPlayers(id_tournament)
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "2. countPlayers() returns 0 after initial deletePlayers() execution."
    player1 = registerPlayer("Chandra Nalaar")
    registerPlayerInTournament(id_tournament,player1)
    c = countPlayers(id_tournament)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1. Got {c}".format(c=c))
    print "3. countPlayers() returns 1 after one player is registered."
    player2 = registerPlayer("Jace Beleren")
    registerPlayerInTournament(id_tournament,player2)
    c = countPlayers(id_tournament)
    if c != 2:
        raise ValueError(
            "After two players register, countPlayers() should be 2. Got {c}".format(c=c))
    print "4. countPlayers() returns 2 after two players are registered."
    deletePlayersInTournament()
    c = countPlayers(id_tournament)
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "5. countPlayers() returns zero after registered players are deleted.\n5. Player records successfully deleted."

def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    id_tournament = registerTournament('test 2')
    player1 = registerPlayer("Melpomene Murray")
    registerPlayerInTournament(id_tournament,player1)
    player2 = registerPlayer("Randy Schwartz")
    registerPlayerInTournament(id_tournament,player2)
    standings = playerStandings(id_tournament)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have five columns.")
    [(id1, name1, wins1, matches1, id_player_tournament1), (id2, name2, wins2, matches2, id_player_tournament2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."

def testReportMatches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    id_tournament = registerTournament('test 3')
    player1 = registerPlayer("Bruno Walton")
    registerPlayerInTournament(id_tournament,player1)
    player2 = registerPlayer("Boots O'Neal")
    registerPlayerInTournament(id_tournament,player2)
    player3 = registerPlayer("Cathy Burton")
    registerPlayerInTournament(id_tournament,player3)
    player4 = registerPlayer("Diane Grant")
    registerPlayerInTournament(id_tournament,player4)
    standings = playerStandings(id_tournament)
    [id1, id2, id3, id4 ] = [row[4] for row in standings]
    reportMatch(id1, id2, id_tournament)
    reportMatch(id3, id4, id_tournament)
    standings = playerStandings(id_tournament)
    for (i, n, w, m, it) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."
    deleteMatchesInTournament(id_tournament)
    standings = playerStandings(id_tournament)
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (i, n, w, m, it) in standings:
        if m != 0:
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "8. After match deletion, player standings are properly reset.\n9. Matches are properly deleted."

def testEvenPairings():
    """
    Test Even pairings are generated properly both before and after match reporting.
    """
    print '---------Test Even pairings---------'
    id_tournament = registerTournament('test 4')
    player = registerPlayer("Twilight Sparkle")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Fluttershy")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Applejack")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Pinkie Pie")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Rarity")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Rainbow Dash")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Princess Celestia")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Princess Luna")
    registerPlayerInTournament(id_tournament,player)
    standings = playerStandings(id_tournament)
    [id1, id2, id3, id4, id5, id6, id7, id8 ] = [row[4] for row in standings]
    pairings = swissPairings(id_tournament)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(id1, id2, id_tournament)
    reportMatch(id3, id4, id_tournament)
    reportMatch(id5, id6, id_tournament)
    reportMatch(id7, id8, id_tournament)
    pairings = swissPairings(id_tournament)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "10. After one match, players with one win are properly paired."

def testOddPairings():
    """
    Test Even pairings are generated properly both before and after match reporting.
    """
    print '---------Test Odd pairings---------'
    id_tournament = registerTournament('test 4')
    player = registerPlayer("Twilight Sparkle")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Fluttershy")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Applejack")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Pinkie Pie")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Rarity")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Rainbow Dash")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Princess Celestia")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Princess Luna")
    registerPlayerInTournament(id_tournament,player)
    player = registerPlayer("Princess Luna 2")
    registerPlayerInTournament(id_tournament,player)
    standings = playerStandings(id_tournament)
    [id1, id2, id3, id4, id5, id6, id7, id8, id9] = [row[4] for row in standings]
    pairings = swissPairings(id_tournament)
    if len(pairings) != 4:
        raise ValueError(
            "For Nine players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(id1, id2, id_tournament)
    reportMatch(id3, id4, id_tournament)
    reportMatch(id5, id6, id_tournament)
    reportMatch(id7, id8, id_tournament)
    if hasBye(id9, id_tournament) != False:
        raise ValueError(
            "For Nine players, swissPairings the last one player should have one Bye.")
    pairings = swissPairings(id_tournament)
    if len(pairings) != 4:
        raise ValueError(
            "For Nine players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id1, id9]),
                          frozenset([id3, id5]), frozenset([id3, id7]),
                          frozenset([id3, id9]), frozenset([id5, id7]),
                          frozenset([id5, id9]), frozenset([id2, id4]), 
                          frozenset([id2, id6]), frozenset([id2, id8]), 
                          frozenset([id4, id6]), frozenset([id4, id8]), 
                          frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            print "13. After two matches, prevent a rematch and create another match"

    standings = playerStandings(id_tournament)
    countBye = 0
    for row in standings:
        if not hasBye(row[4], id_tournament):
            countBye+= 1
    if countBye != 2:
        raise ValueError(
            "After two matches, there going to be two byes from differents users")
    print "14. After two matches, there are two byes."

if __name__ == '__main__':
    tesDetele()
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testEvenPairings()
    testOddPairings()
    print "Success!  All tests pass!"
