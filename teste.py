from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense



model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.save("model.h5")
print("Saved model to disk")