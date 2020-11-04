from threading import main_thread
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException

def _establish_connection_to_aml_workspace():
    try:
        ws=Workspace.from_config(r'set_up_aml\config.json')
        return ws
    except Exception as e:
        raise e

def _get_compute_target(ws,compute_target_name):
    try:
        compute_target = ComputeTarget(workspace=ws, name=compute_target_name)
        return compute_target
    except Exception as e:
        raise e

def _get_list_of_models(ws,name=None):
    return Model.list(workspace=ws,name=name)


