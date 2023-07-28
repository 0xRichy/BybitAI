from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import logging

class MachineLearningModel:
    def __init__(self):
        self.classifier = Sequential()
        self.classifier.add(Dense(units = 64, kernel_initializer = 'uniform', activation = 'relu', input_dim = 10))
        self.classifier.add(Dense(units = 64, kernel_initializer = 'uniform', activation = 'relu'))
        self.classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))
        self.classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

    def create_dataset(self, data, window_size):
        X, y = [], []
        for i in range(len(data) - window_size - 1):
            window = data[i:i+window_size]
            X.append(window)
            y.append(1 if data[i+window_size] > self.generate_ai_indicator(window) else -1)
        return np.array(X), np.array(y)

    def train(self, X, y):
        self.classifier.fit(X, y, batch_size = 10, epochs = 100)
        logging.info("Classifier trained successfully at {time.time()}")

    def predict(self, data):
        prediction = self.classifier.predict(np.array([data]))[0]
        logging.info(f"Prediction made: {prediction} at {time.time()}")
        return prediction
