
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Activation


class ChessEvaluator():

    def __init__(self, load_model=None):

        if load_model:
            # Load model
            pass
        else:
            #create model
            self._model = Sequential()
            self._model.add(Conv2D(20, kernel_size=5, input_shape=(15,8,8)))
            self._model.add(Activation())
            self._model.add(Conv2D(50, kernel_size=3, activation='relu'))
            self._model.add(Flatten())
            self._model.add(Dense(500, activation='relu'))
            self._model.add(Dense(1))

    def train(train_X, train_Y, epochs=5):
        self._model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])