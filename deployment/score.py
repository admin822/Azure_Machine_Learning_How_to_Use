from azureml.core import databricks
import torch
import json
import os
from deployment.dummy import dummy_model
from deployment.deployment_exception import json_process_exception,prediction_exception



def init():
    try:
        global model
        model=dummy_model()
        model_path=os.path.join(os.getenv('AZUREML_MODEL_DIR'),'saved_model.pt')
        model.load_state_dict(torch.load(model_path))
    except Exception as e:
        print("Failed to initialize deployment due to {}".format(e))

def _process_input_json_file(data):
    try:
        deserialized_data=json.loads(data) # a list
        deserialized_data=torch.tensor(deserialized_data['data_field']).float()
        return deserialized_data
    except Exception as e:
        raise json_process_exception(str(e))

def _predict(deserialized_data):
    try:
        with torch.no_grad():
            model.eval()
            return model(deserialized_data).tolist()
    except Exception as e:
        raise prediction_exception(str(e))


def run(data):
    try:
        deserialized_data=_process_input_json_file(data)
    except Exception as e:
        return "failed to deserialize json input due to {}".format(e)
    try:
        result=_predict(deserialized_data)
        return result
    except json_process_exception as e:
        return "input data processing failed due to {}".format(e)
    except prediction_exception as e:
        return "prediction failed due to {}".format(e)