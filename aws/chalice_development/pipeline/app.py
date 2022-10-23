
import numpy as np
import pickle
from chalice import Chalice
import boto3



s3 = boto3.client('s3')
s3_bucket = "pickle1234"
model_name = "iris_model.pkl"
temp_file_path = '/tmp/' + model_name

app = Chalice(app_name='pipeline')

key = 'iris_model.pkl'





@app.route('/',methods=['POST'])
def index():

    
    data=user=app.current_request.json_body
    print("data::",data)

    if 'a' in data.keys() and 'b' in data.keys() and 'c' in data.keys() and 'd' in data.keys():
        
        features=[data['a'],data['b'],data['c'],data['d']]
        np_features=[np.asarray(features)]

        print(np_features)

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



