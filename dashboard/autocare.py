from dashboard.method import CompanyMethod, ConfigMethod, ModelMethod
import tensorflow as tf
import numpy as np
import datetime
from sklearn.model_selection import train_test_split
import pandas as pd
from .logger import logger

class autocare():
    def learning(model_id, case):
        # case - 0: 자동학습 1: 강제학습
        model_data = ModelMethod.get(model_id)
        model_name = model_data.model_name
        model_path = model_data.model_path
        model_file = model_path + model_data.model_file
        model = tf.keras.models.load_model(model_file)
        dataset = pd.read_csv(model_data.data_path)

        x_data = dataset.iloc[:,:-1]
        y_data = dataset.iloc[:,-1]

        x_data = np.array(x_data)
        y_data = np.array(y_data)

        x_data = x_data.reshape(-1,125,1)
        y_data = tf.keras.utils.to_categorical(y_data,2)

        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, train_size=0.8, random_state=1, shuffle=True)

        model.fit(x_train,y_train,epochs=1,batch_size=128, validation_data=(x_test, y_test))

        now = datetime.datetime.now()
        format = '%Y%m%d%H%M%S%Z'
        file_date = datetime.datetime.strftime(now,format)

        new_rname =  model_data.model_rname + '_' + file_date + '.h5'

        print(new_rname)

        ModelMethod.set(model_id=model_id,model_file=new_rname)

        model.save(model_path + new_rname)
        if case == 0:
            logger.update_model(model_name)
        else:
            logger.auto_update_model(model_name)


        return