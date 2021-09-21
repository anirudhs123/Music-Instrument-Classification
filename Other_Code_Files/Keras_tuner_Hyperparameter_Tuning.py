
! pip install keras-tuner

import tensorflow as tf
from tensorflow import keras

#Building model
from keras.layers import Dense,LeakyReLU,ELU,PReLU,Dropout,Conv2D
from keras.models import Sequential
def  build_model(hp):
  model=keras.Sequential([
                          keras.layers.Conv2D(filters=hp.Int('Conv_1_filter',min_value=32,max_value=64,step=16),
                                              kernel_size=hp.Choice('Convo_1_kernels',values=[3,5]),
                                              activation='relu',
                                              input_shape=(X_train.shape[1],X_train.shape[2],1)),
                           keras.layers.Conv2D(filters=hp.Int('Conv_1_filter',min_value=64,max_value=128,step=16),
                                              kernel_size=hp.Choice('Convo_1_kernels',values=[3,5]),
                                              activation='relu'),
                                              
                           keras.layers.Conv2D(filters=hp.Int('Conv_1_filter',min_value=128,max_value=256,step=16),
                                              kernel_size=hp.Choice('Convo_1_kernels',values=[3,5]),
                                              activation='relu'),
                                              
                           keras.layers.Conv2D(filters=hp.Int('Conv_1_filter',min_value=256,max_value=512,step=16),
                                              kernel_size=hp.Choice('Convo_1_kernels',values=[3,5]),
                                              activation='relu'),
                          
                          keras.layers.Flatten(),
                          keras.layers.Dense(units=hp.Int('Dense_1_units',max_value=128,min_value=64,step=16),
                                             activation='relu'
                                             ),
                          
                          keras.layers.Dense(units=1,
                                             activation='linear'
                                             )
                          
                                             ])
  model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
  model.summary()
  return(model)

from kerastuner import RandomSearch
import kerastuner.engine.hyperparameters as Hyperparameters

tuner_search=RandomSearch(build_model,
                          objective='val_mean_absolute_error',
                          max_trials=5
                          )
tuner_search.search(X_train,y_train_coord,epochs=3,validation_split=0.1)
model=tuner_search.get_best_models(num_models=1)[0]
model.fit(X_train,y_train_coord,epochs=500,validation_split=0.2,initial_epoch=3)

preds_y=model.predict(X_test)