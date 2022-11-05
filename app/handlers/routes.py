import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os
import sys

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"

    @app.route('/predict')
    def predict():
        #use entries from the query string here but could also use json
        age = request.args.get('age')
        absences = request.args.get('absences')
        health = request.args.get('health')
        studytime = request.args.get('studytime')

        if int(health) < 1 or int(health) > 5:
            result = "hi ur health parameter is outta bounds."
            return result, 500
        if int(absences) < 0 or int(absences) > 93:
            result = "hi ur absences parameter is outta bounds."
            return result, 500
        if int(age) < 15 or int(age) > 22:
            result = "hi ur age parameter is outta bounds."
            return result, 500
        if int(studytime) < 0:
            result = "hi ur health parameter is outta bounds."
            return result, 500

        data = [[age], [health], [absences], [studytime]]
        query_df = pd.DataFrame({
            'age': pd.Series(age),
            'health': pd.Series(health),
            'absences': pd.Series(absences),
            'studytime': pd.Series(studytime)
        })
        
        # Converting the dataframe into a one-hot encoded dataframe.)
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        print(prediction)
        sys.stdout.flush()
        return jsonify(np.ndarray.item(prediction))

    @app.route('/batch')
    def batch():
        # what's going to come in is "studentid1,studentid2"
        bigstring = request.args.get('applicant_info')
        def comma_separated_params_to_list(param):
            result = []
            for val in param.split(','):
                if val:
                    result.append(val)
            return result

        def underscore_separated_params_to_list(param):
            result = []
            for val in param.split('_'):
                if val:
                    result.append(val)
            return result
     
        perapplicant = comma_separated_params_to_list(bigstring)

        count = 0
        for applicant in perapplicant:
            temps = underscore_separated_params_to_list(applicant)
            if len(temps) > 4 or len(temps) < 4:
                result = "hi you're passing in the wrong number of parameters."
                return result, 500

            age = temps[0]
            absences = temps[1]
            health = temps[2]
            studytime = temps[3]

            if int(health) < 1 or int(health) > 5:
                result = "hi ur health parameter is outta bounds."
                return result, 500
            if int(absences) < 0 or int(absences) > 93:
                result = "hi ur absences parameter is outta bounds."
                return result, 500
            if int(age) < 15 or int(age) > 22:
                result = "hi ur age parameter is outta bounds."
                return result, 500
            if int(studytime) < 0:
                result = "hi ur health parameter is outta bounds."
                return result, 500

            data = [[age], [health], [absences], [studytime]]
            query_df = pd.DataFrame({
                'age': pd.Series(age),
                'health': pd.Series(health),
                'absences': pd.Series(absences),
                'studytime': pd.Series(studytime)
            })
            query = pd.get_dummies(query_df)
            prediction = clf.predict(query)
            if np.ndarray.item(prediction) == 1:
                count += 1
        return jsonify(count)

