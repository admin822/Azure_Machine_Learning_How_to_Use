from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import Environment
from azureml.core import ScriptRunConfig
from azureml.core import Dataset
import os
from util import _establish_connection_to_aml_workspace,_get_compute_target


def _create_running_config(ws:Workspace,path_to_dataset_in_datastore,compute_target_name,env_name,model_save_path):
    try:
        module_root_folder_path=r'online_training'
        compute_target=_get_compute_target(ws,compute_target_name)
        default_data_store=ws.get_default_datastore()
        dataset=Dataset.File.from_files(path=(default_data_store,path_to_dataset_in_datastore))
        module_env=Environment.get(workspace=ws,name=env_name)

        running_config=ScriptRunConfig(source_directory=module_root_folder_path,
        script='train.py',
        compute_target=compute_target,
        environment=module_env,
        arguments=[
            "--data_path",dataset.as_mount(),
            "--batch_size",32,
            "--model_path",model_save_path
        ]
        )
        print("running config created!")
        return running_config
    except Exception as e:
        raise e


def submit_experiment(path_to_dataset_in_datastore,compute_target_name,experiment_name,env_name,model_name,model_save_path):
    try:
        ws=_establish_connection_to_aml_workspace()
    except Exception as e:
        raise e
    try:
        experiment=Experiment(workspace=ws,name=experiment_name)
        running_config=_create_running_config(ws,path_to_dataset_in_datastore,compute_target_name,env_name,model_save_path)
        
        ############### submit experiment and get url ################
        run=experiment.submit(running_config)
        url=run.get_portal_url()
        print("The details for this experiment is here:\n {}".format(url))
        run.wait_for_completion()
        print("Experiment run has completed, Note:This message does NOT suggetst your experiment is successful, go to {} to find out logs and status for your experiment".format(url))
        ############### submit experiment and get url ################
    except Exception as e:
        print("Submit Experiment failed!")
        raise e
    try:
        ############### register model ######################
        run.register_model(model_name=model_name,model_path=os.path.join(model_save_path,'saved_model.pt'))
    except Exception as e:
        print("Failed to register due to {}!".format(e))

    
        




if __name__ == "__main__":
    submit_experiment(path_to_dataset_in_datastore='dummy/dummy_data_file',
                compute_target_name="testConfDSVM", 
                # compute_target_name="StandardCompute",
                experiment_name="test_trial1",
                env_name="confidential_test",
                model_name="dummy_test_model",
                model_save_path='./outputs')
