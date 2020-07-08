from tournament.swiss import SwissTournament
from tournament.Player import Player
from tournament.games import halite_game


def main():
    # create 10 random players
    num_players = 20
    players = [Player(i) for i in range(num_players)]

    tourn = SwissTournament(7, players, 4, halite_game, 100)

    tourn.run()

    print(tourn.get_scores)


if __name__ == '__main__':
    main()
