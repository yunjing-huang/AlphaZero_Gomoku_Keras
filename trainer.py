import numpy as np
from random import shuffle
import time
from monte_carlo_tree_search import MCTS

class Trainer():
    def __init__(self, game, model, args):
        self.game = game
        self.model = model
        self.args = args
        self.mcts = MCTS(self.game, self.model, self.args)
    def exceute_episode(self):
        train_examples = []
        current_player = 1
        state = self.game.get_init_board()
        while True:
            canonical_board = self.game.get_canonical_board(state, current_player)
            self.mcts = MCTS(self.game, self.model, self.args)
            root = self.mcts.run(self.model, canonical_board, to_play=1)
            action_probs = [0 for _ in range(self.game.get_action_size())]
            for k, v in root.children.items():
                action_probs[k] = v.visit_count
            action_probs = action_probs / np.sum(action_probs)
            train_examples.append((canonical_board, current_player, action_probs))
            action = root.select_action(temperature=0)
            state, current_player = self.game.get_next_state(state, current_player, action)
            reward = self.game.get_reward_for_player(state, current_player)
            if reward is not None:
                ret = []
                for hist_state, hist_current_player, hist_action_probs in train_examples:
                    ret.append((hist_state, hist_action_probs, reward * ((-1) ** (hist_current_player != current_player))))
                return ret
    def learn(self):
        for i in range(1, self.args['numIters'] + 1):
            print("{}/{}".format(i, self.args['numIters']))
            train_examples = []
            for eps in range(self.args['numEps']):
                start = time.time()
                iteration_train_examples = self.exceute_episode()
                train_examples.extend(iteration_train_examples)
                print("one episode takes {}s".format(time.time()-start))
            shuffle(train_examples)
            self.train(train_examples)
            self.model.model.save("C:/Users/Yunji/PycharmProjects/python1/gomoku/model/model_{:05d}_iters".format(i))
    def train(self, examples):
        input_boards, target_pis, target_vs = list(zip(*examples))
        input_boards = np.asarray(input_boards)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)
        self.model.model.fit(x=input_boards, y=[target_pis, target_vs], batch_size=self.args["batch_size"], epochs=self.args["epochs"])


