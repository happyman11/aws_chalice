import os
import numpy as np
import pickle
from chalice import Chalice
import boto3
import json

'''
{
  
  "a":1,
  "b":2,
  "c":3,
  "d":4
}
'''

s3 = boto3.client('s3')
s3_bucket = "pickle1234"
model_name = "iris_model.pkl"
temp_file_path = '/tmp/' + model_name

app = Chalice(app_name='pipeline')

key = 'iris_model.pkl'





@app.route('/',methods=['POST'])
def index():

    
    data=user=app.current_request.json_body
    

    if 'a' in data.keys() and 'b' in data.keys() and 'c' in data.keys() and 'd' in data.keys():
        
        features=[data['a'],data['b'],data['c'],data['d']]
        np_features=[np.asarray(features)]

        s3.download_file(s3_bucket, model_name, temp_file_path)
        with open(temp_file_path, 'rb') as f:
            model = pickle.load(f)
            
        prediction = model.predict(np_features)
        labels = ['setosa', 'versicolor', 'virginica']

        result = labels[prediction[0]]

        print(result)

        return {'Label of flower is': result}

    else:

        return {'Dear User': "Pleacke check the Paylaod"}



    
    
@app.route('/{username}', methods=['GET'])
def get_user(username):

    dir=os.listdir()
    
    return {'name':json.dumps(dir)}



# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
