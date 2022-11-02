import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

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
        data = [[age], [health], [absences]]
        query_df = pd.DataFrame({
            'age': pd.Series(age),
            'health': pd.Series(health),
            'absences': pd.Series(absences)
        })
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        return jsonify(np.ndarray.item(prediction))

    @app.route('/batch')
    def predictBatch():
        # what's going to come in is "studentid1,studentid2"

        bigstring = request.args['applicant_info']
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
            age = temps[0]
            absences = temps[1]
            health = temps[2]
            data = [[age], [health], [absences]]
            query_df = pd.DataFrame({
                'age': pd.Series(age),
                'health': pd.Series(health),
                'absences': pd.Series(absences)
            })
            query = pd.get_dummies(query_df)
            prediction = clf.predict(query)
            if np.ndarray.item(prediction) == 1:
                count += 1
        return jsonify(count)

        # request_data = {}
        # params = request.args.getlist('status') or request.form.getlist('status')
        # if len(params) == 1 and ',' in params[0]:
        #     request_data['status'] = comma_separated_params_to_list(params[0])
        # else:
        #     request_data['status'] = params

        # age = request.args.get('age')
        # absences = request.args.get('absences')
        # health = request.args.get('health')
        # data = [[age], [health], [absences]]
        # query_df = pd.DataFrame({
        #     'age': pd.Series(age),
        #     'health': pd.Series(health),
        #     'absences': pd.Series(absences)
        # })
        # query = pd.get_dummies(query_df)
        # prediction = clf.predict(query)
        # return jsonify(np.asscalar(prediction))

