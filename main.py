from game import Gomoku
from model import GomokuModel
from trainer import Trainer

args = {
    'batch_size': 64,
    'numIters': 1000,                                # Total number of training iterations
    'num_simulations': 25,                         # Total number of MCTS simulations to run when deciding on a move to play
    'numEps': 100,                                  # Number of full games (episodes) to run during each iteration
    'epochs': 10,                                    # Number of epochs of training per iteration
}

game = Gomoku()
model = GomokuModel(game)

trainer = Trainer(game, model, args)
trainer.learn()
