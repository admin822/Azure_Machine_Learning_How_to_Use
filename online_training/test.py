import json
import torch
from dummy import dummy_model

def func(json_data):
    model=dummy_model()
    model.eval()
    with torch.no_grad():
        data=json.loads(json_data)['data_field']
        data=torch.tensor(data).float()
        result=model(data).tolist()
        print(result)
    


if __name__ == "__main__":
    test_data=json.dumps({'data_field':[1,123,123,41,3,123,123,4,1,5]})
    print(type(test_data))
    print(test_data)
    func(test_data)
