from flask import Flask, request, jsonify, render_template, url_for
import requests
import json

# app = Flask(__name__)
app=Flask(__name__,template_folder='./')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/azure-ml-api', methods=['POST'])
def azure_ml_api():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        print(data)

        # Check if 'inputs' is present in the JSON
        if 'inputs' not in data:
            return jsonify({'error': 'Missing required attributes "inputs" or "parameters"'}), 400

        

        # Construct the endpoint URL
        endpoint_name = "my-endpoint" # Replace with your endpoint name
        endpoint_url = f"https://question-answering-opschatbot.eastus2.inference.ml.azure.com/score"

        # Set the authorization header
        subscription_key = "<<REPLACE>>" # Replace with your subscription key
        headers = {"Authorization": f"Bearer {subscription_key}"}

        # Send a POST request to the endpoint
        response = requests.post(endpoint_url, headers=headers, json=data)

        # Return the response from the endpoint as a JSON response
        return jsonify(response.json())

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/local-ml-api', methods=['POST'])
def local_ml_api():
    try:
        # Get the JSON data from the request
        
        question = request.form.get('question')
        context = request.form.get('context')
        requestObject = {
            'inputs': {
                'question': [],
                'context': []
            }
        }
        # Add elements to 'question' and 'context'
        requestObject['inputs']['question'].append(question)
        requestObject['inputs']['context'].append(context)
       
        print(json.dumps(requestObject))

        # Construct the endpoint URL
        endpoint_name = "my-endpoint" # Replace with your endpoint name
        endpoint_url = f"https://question-answering-opschatbot.eastus2.inference.ml.azure.com/score"

        # Set the authorization header
        subscription_key = "yaaA7zeQ1QeaIU04KDazvVoj3rdzwXQq" # Replace with your subscription key
        headers = {"Authorization": f"Bearer {subscription_key}"}

        # Send a POST request to the endpoint
        response = requests.post(endpoint_url, headers=headers, json=requestObject)
        print(response.json())
        print('1', response.json()[0]['answer'])
       
       
        # Return the response from the endpoint as a JSON response       
        #return render_template('home.html', prediction_text="AQI for Jaipur {}".format(json.dumps(response.json()[0])))
        return render_template('./index.html', answer=response.json()[0]['answer'], start=response.json()[0]['start'],end=response.json()[0]['end'],
                               score=response.json()[0]['score'])

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
