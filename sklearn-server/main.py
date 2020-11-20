import numpy as np
import pandas as pd
from utils import transform, postprocess, predict
from flask import jsonify, request, Flask
import joblib
import pickle


# app = Flask(__name__)

# @app.route('/pred', methods=['GET', 'POST'])
def lrc_model(request):
    

    # encoders_dict = {}
    # download_blob('police-shootings', 'model/model.joblib', 'model.joblib')
    # for col in cat_cols:
    #     download_blob('police-shootings', f'encoders/{col}_encoder.pkl', f'{col}_encoder.pkl')
    if request.method == 'OPTIONS':
        
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        
        return (' ', 204, headers)

        

    if request.method == 'POST':
        instances = request.json['instances']
        instances = [transform(instance) for instance in instances]
        predictions = predict(instances)
        result = postprocess(predictions)
        
        headers = {
            'Access-Control-Allow-Origin': '*',
            # 'Access-Control-Allow-Methods': 'POST',
            # 'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Credentials': 'true'
            # 'Access-Control-Max-Age': '3600'
            
        }
        return (jsonify({"predictions": result, "probabilities": predictions}), 200,  headers)

