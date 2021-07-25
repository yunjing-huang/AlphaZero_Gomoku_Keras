from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import *
import numpy as np
class GomokuModel():
    def __init__(self, game):
        self.board_x, self.board_y = game.get_board_size()
        self.action_size = game.get_action_size()
        self.input_boards = Input(shape=(self.board_x, self.board_y))
        x_image = Reshape((self.board_x, self.board_y, 1))(self.input_boards)
        h_conv1 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(512, 3, padding='same')(x_image)))
        h_conv2 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(512, 3, padding='same')(h_conv1)))
        h_conv3 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(512, 3, padding='valid')(h_conv2)))
        h_conv4 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(512, 3, padding='valid')(h_conv3)))
        h_conv4_flat = Flatten()(h_conv4)
        s_fc1 = Dropout(0.3)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024)(h_conv4_flat))))
        s_fc2 = Dropout(0.3)(Activation('relu')(BatchNormalization(axis=1)(Dense(512)(s_fc1))))
        self.pi = Dense(self.action_size, activation='softmax', name='pi')(s_fc2)
        self.v = Dense(1, activation='tanh', name='v')(s_fc2)
        self.model = Model(inputs=self.input_boards, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=Adam(0.0005))
    def predict(self, board):
        board = board[np.newaxis, :, :]
        pi, v = self.model.predict(board)
        return pi[0], v[0]
