from tournament.swiss import SwissTournament


def test_game(p):
    return [1, 0,0]


players = range(0,10)

tourn = SwissTournament(7, players, 3, test_game)

tourn._rounds_played = 1
tourn._scores[0][0] = 1

print(tourn.get_scores)

print(tourn.get_tiebreaks)

print(tourn.get_standings_by_index())

print(tourn.get_tiebreaks.max())

tourn.run()
