import joblib
import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from prometheus_flask_exporter import PrometheusMetrics

#from model.train import train_model

app = Flask(__name__)
api = Api(app)
metrics = PrometheusMetrics(app, group_by='endpoint')

if not os.path.isfile('../model/credit-card-fraud-model.model'):
    print('model not found!!')
    #train_model()

loaded_model = joblib.load('../model/credit-card-fraud-model.model')

@app.route('/predict')
@metrics.counter('predict', 'Number of prediction',
         labels={'result': lambda: request.predicted_class})
def predict():
    posted_data = request.get_json()
    transaction_info = posted_data['transaction_detail']

    prediction = loaded_model.predict([transaction_info])[0]

    if prediction == 0:
        request.predicted_class = 'normal'
    else:
        request.predicted_class = 'fraud'

    return jsonify({
        'Prediction': request.predicted_class
    })


# class MakePrediction(Resource):
#     @staticmethod
#     def post():
#         posted_data = request.get_json()
#         transaction_info = posted_data['transaction_detail']

#         prediction = loaded_model.predict([transaction_info])[0]

#         if prediction == 0:
#             predicted_class = 'Normal Transaction 1'
#         else:
#             predicted_class = 'Fraud Transaction'

#         return jsonify({
#             'Prediction': predicted_class
#         })

# api.add_resource(MakePrediction, '/predict')


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)