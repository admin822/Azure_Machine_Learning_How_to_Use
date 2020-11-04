import requests
import json

if __name__ == "__main__":
    scoring_uri='http://202b7995-5a51-4923-9d2e-c4114e7bd28d.southeastasia.azurecontainer.io/score'
    headers = {'Content-Type':'application/json'}
    test_data=json.dumps({'data_field':[1,123,123,41,3,123,123,4,1,5]})
    response = requests.post(scoring_uri, data=test_data, headers=headers)
    print(response.status_code)
    print(response.elapsed)
    print(response.json())
