#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."

def testCheckMatch():
    deleteMatches()
    deletePlayers()
    registerPlayer("Jack Sparrow")
    registerPlayer("Mickey Mouse")
    standings = playerStandings()
    [id1, id2] = [row[0] for row in standings]   
    if checkMatch(id1,id2):
        raise ValueError(
            "If players did not have a match, getMatch should return False.")
    reportMatch(id1, id2)
    if not checkMatch(id1,id2):
        raise ValueError(
            "Match happened, getMatch should return True.")
    print "9. It is possible to check if a match happened or not"

def testNonRepeatMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id1, id3)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid4, pname4), (pid2, pname2, pid3, pname3)] = pairings
    correct_pairs = set([frozenset([id1, id4]), frozenset([id2, id3])])
    actual_pairs = set([frozenset([pid1, pid4]), frozenset([pid2, pid3])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "Players that already played should not be matched.")
    print "10. Repeated matches are avoided, if possible. Matching on " \
          "4 players scenario would be 1x4 and 2x3, in case winners already played."

def testExtremeRepeatMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id1, id3)
    reportMatch(id1, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    print "11. When there is no way to avoid repetition, return a pairing anyways."

def testOpponentMatchWinsRanking():
    deleteMatches()
    deletePlayers()
    registerPlayer("Aaron")
    registerPlayer("Barry")
    registerPlayer("Charlie")
    registerPlayer("David")
    registerPlayer("Edward")
    registerPlayer("Frank")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6] = [row[0] for row in standings]
    reportMatch(id1, id4)
    reportMatch(id2, id5)
    reportMatch(id3, id6)
    pairings = swissPairings()
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), \
    (pid5, pname5, pid6, pname6)] = pairings
    correct_pairs = set([frozenset([id1, id2]), frozenset([id3, id4]), \
        frozenset([id5, id6])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), \
        frozenset([pid5, pid6])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "Matching from 6 players is incorrect.")
    # now report a match where loser of id3 has a win, 
    # so id3 goes to first place
    # id6 will also have one win, so it goes up in the standings, resulting in:
    # 3 > 1 == 2 == 6 > 4 == 5
    reportMatch(id6, id5)
    pairings = swissPairings()
    [(pid3, pname3, pid1, pname1), (pid2, pname2, pid6, pname6), \
    (pid4, pname4, pid5, pname5)] = pairings
    correct_pairs = set([frozenset([id3, id1]), frozenset([id2, id6]), \
        frozenset([id4, id5])])
    actual_pairs = set([frozenset([pid3, pid1]), frozenset([pid2, pid6]), \
        frozenset([pid4, pid5])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "The Oponent Match Wins is not being used in ranking sorting.")
    print "12. The pairings take in consideration the opponent match wins."

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testCheckMatch()
    testNonRepeatMatches()
    testExtremeRepeatMatches()
    testOpponentMatchWinsRanking()
    print "Success!  All tests pass!"


