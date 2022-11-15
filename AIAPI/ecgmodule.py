import numpy as np
import tensorflow as tf
import json

# 부정맥 판단 모델
class CAmodel():
    def __init__(self):
        self.user_id = -1
        self.user_data = None
        self.model = tf.keras.models.load_model('static/model/CAModel_v1.3_acc0.76_rec0.75_221101.h5')
        self.pred_classes = ['정상','비정상']
        print("Load ECG model")
        
    def get_result(self, user_data):
        raw_data = np.array(user_data)
        label_data = self.analysis_data(raw_data)
        result = self.predict(label_data)
        return result
    
    def analysis_data(self, raw_data):

        if len(raw_data) >= 125:
            raw_data = raw_data[:125]
        elif len(raw_data) < 125:
            temp_length = 125 - len(raw_data)
            temp_arr = np.zeros(shape=(temp_length,))
            raw_data = np.concatenate((raw_data, temp_arr), axis=0)

        min_data = min(raw_data)
        max_data = max(raw_data)
        
        label_data = raw_data - min_data
        label_data = label_data / max_data
        return label_data

    def predict(self, label_data):
        label_data = label_data.reshape(-1,len(label_data),1)
        prob = self.model.predict(label_data, verbose=0)
        
        result_prob = prob.argmax(axis=-1)
        result_prob = result_prob[0]
        # print("result_prob: "+str(result_prob))
        result = self.pred_classes[result_prob]

        class_prob = prob[0][result_prob]
        class_prob = class_prob * 100


        return class_prob, result_prob, result
        


# 심부전 판단 모델
class HFmodel():
    def __init__(self):
        self.user_id = -1
        self.user_data = None
        self.model = tf.keras.models.load_model('static/model/HFModel_v1.2_acc0.86_221021.h5')
        self.pred_classes = ['정상','비정상']
        print("Load ECG model")
        
    def get_result(self, user_data):
        raw_data = np.array(user_data)
        label_data = self.analysis_data(raw_data)
        result = self.predict(label_data)
        return result
    
    def analysis_data(self, raw_data):

        if len(raw_data) >= 125:
            raw_data = raw_data[:125]
        elif len(raw_data) < 125:
            temp_length = 125 - len(raw_data)
            temp_arr = np.zeros(shape=(temp_length,))
            raw_data = np.concatenate((raw_data, temp_arr), axis=0)

        min_data = min(raw_data)
        max_data = max(raw_data)
        
        label_data = raw_data - min_data
        label_data = label_data / max_data
        return label_data

    def predict(self, label_data):
        label_data = label_data.reshape(-1,len(label_data),1)
        prob = self.model.predict(label_data, verbose=0)
        
        result_prob = prob.argmax(axis=-1)


        result_prob = result_prob[0]
        result = self.pred_classes[result_prob]

        class_prob = prob[0][result_prob]
        class_prob = class_prob * 100


        return class_prob, result_prob, result