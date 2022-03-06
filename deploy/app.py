from flask import Flask,request
from waitress import serve
from prometheus_flask_exporter import PrometheusMetrics

import random

app = Flask(__name__)
metrics = PrometheusMetrics(app, group_by='endpoint')
percentage=1

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/setFraudPercentage')
def setFraudPercentage():
	percentage= request.args.key("value")
    
    return "Fraud percentage changed" 

@app.route('/predict')
@metrics.counter('predict', 'Number of prediction',
         labels={'result': lambda: request.result})
def predict():
	top = 100/percentage
	request.result = 'invalid'
	number = random.randint(0,top)
	if number == 0:
	 request.result = 'fraud'
	else:
	  request.result = 'normal'
	return request.result

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
