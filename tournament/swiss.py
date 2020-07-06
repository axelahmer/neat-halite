import numpy as np
import tournament.Player
from concurrent.futures import ProcessPoolExecutor

class SwissTournament(object):
    def __init__(self, num_rounds, players, players_per_game, game_pointer, bye_award=1):
        # run game must be thread-safe
        self._run_game = game_pointer
        self._bye_award = bye_award
        self._players_per_game = players_per_game
        self._pairings_per_round = len(players) // players_per_game
        self._byes_per_round = len(players) % players_per_game
        self._num_rounds = num_rounds
        self._completed_rounds = 0
        self._players = players
        self._scores = np.zeros((len(players), num_rounds), dtype=np.float)
        self._pairings = []
        self._byes = []
        self._opponents = np.zeros((len(players), len(players)), dtype=np.float)

    @property
    def get_scores(self):
        return self._scores[:, :self._completed_rounds].sum(axis=1)

    @property
    def get_tiebreaks(self):
        return np.matmul(self._opponents, self._scores.sum(axis=1, keepdims=True)).ravel()

    def get_standings_by_index(self):
        # returns an array of player in standing order, ranked best to worst
        fraction_ties = self.get_tiebreaks / (self.get_tiebreaks.max() + 1e-8)
        adjusted_scores = np.add(self.get_scores, fraction_ties)
        indices = np.argsort(adjusted_scores)[::-1]
        return list(indices)

    def run(self):
        for rnd in range(self._num_rounds):
            self._pair_round()
            # self._play_round()
            self._play_round_multiprocess()
            self._completed_rounds += 1
            print(f'round {rnd + 1} completed.')
        print(f'tournament completed.')

    def _pair_round(self):
        standings = self.get_standings_by_index()
        pairings = []
        byes = []

        for i in range(0, len(standings), self._players_per_game):
            game_players = list(standings[i:i + self._players_per_game])
            pairings.append(game_players)
        if self._byes_per_round > 0:
            byes = pairings.pop()

        self._pairings.append(pairings)
        self._byes.append(byes)

        # add opponents to opponent table
        for game in pairings:
            for pos, seed in enumerate(game):
                opponent_seeds = game.copy()
                opponent_seeds.pop(pos)
                for opp_seed in opponent_seeds:
                    self._opponents[seed][opp_seed] += 1

    def _play_round(self):
        rnd = len(self._pairings)

        # play games and award scores
        for player_ids in self._pairings[-1]:
            game_players = [self._players[i] for i in player_ids]
            results = self._run_game(game_players)
            for score, player_id in zip(results, player_ids):
                self._scores[player_id][rnd - 1] = score

        # award points to byes
        for player_id in self._byes[-1]:
            self._scores[player_id][rnd - 1] = self._bye_award

    def _play_round_multiprocess(self, max_workers=None):
        rnd = len(self._pairings)

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for seeds in self._pairings[-1]:
                players = [self._players[seed] for seed in seeds]
                future = executor.submit(self._run_game, players)
                futures.append(future)
        rewards = [f.result() for f in futures]
        for seeds, scores in zip(self._pairings[-1], rewards):
            for seed, score in zip(seeds, scores):
                self._scores[seed][rnd-1] = score

        # award points to byes
        for player_id in self._byes[-1]:
            self._scores[player_id][rnd - 1] = self._bye_award
