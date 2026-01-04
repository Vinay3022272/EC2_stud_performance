import os
import sys 
import numpy as np
import pandas as pd
from src.exception import CustomException
from sklearn.metrics import r2_score
import dill
from sklearn.model_selection import GridSearchCV


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        for model_name, model in models.items():
            param = params[model_name]
            grid = GridSearchCV(estimator=model, param_grid=param, cv=3, verbose=3)
            grid.fit(X_train, y_train)
            
            best_model = grid.best_estimator_
            
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            r2_score_train = r2_score(y_train, y_train_pred)
            r2_score_test = r2_score(y_test, y_test_pred)
            
            report[model_name] = r2_score_test
             
        return report 
             
    except Exception as e:
        raise CustomException(e, sys)    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
          return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)

    