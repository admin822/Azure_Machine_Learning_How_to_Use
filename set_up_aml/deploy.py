from azureml.core.model import InferenceConfig
from azureml.core.webservice import LocalWebservice
from azureml.core.webservice import AciWebservice
from azureml.core.model import Model
from azureml.core import Environment
from requests import models
from util import _establish_connection_to_aml_workspace

def _create_inference_config(inference_env_name):
    try:
        ws=_establish_connection_to_aml_workspace()
    except Exception as e:
        print("failed to connect to workspce")
        raise e
    try:
        environment=Environment.get(workspace=ws,name=inference_env_name)
        inference_config=InferenceConfig(entry_script="score.py",
                                            environment=environment,
                                            source_directory=r'deployment')
        return inference_config
    except Exception as e:
        print("failed to create inference config")
        raise e

def _start_deploy_model(inference_config,deployment_config,model_name,model_version,deployment_name):
    try:
        ws=_establish_connection_to_aml_workspace()
    except Exception as e:
        print("failed to connect to workspce")
        raise e
    try:
        model=Model(workspace=ws,name=model_name,version=model_version)
        service=model.deploy(workspace=ws,
                                name=deployment_name,
                                models=[model],
                                inference_config=inference_config,
                                deployment_config=deployment_config,
                                overwrite=True)
        service.wait_for_deployment()
        print(service.state)
        print("Deployed at {}".format(service.scoring_uri))
    except Exception as e:
        raise e

# you need a docker engine running on your local machine.
def depoly_to_local_web(inference_env_name,port_num:int,model_name,model_version,deployment_name):
    try:
        inference_config=_create_inference_config(inference_env_name)
    except Exception as e:
        raise e
    try:
        deployment_config=LocalWebservice.deploy_configuration(port_num)
        _start_deploy_model(inference_config,deployment_config,model_name,model_version,deployment_name)
    except Exception as e:
        print("failed to deploy")
        raise e

## You need to quickly deploy and validate your model. You do not need to create ACI containers ahead of time. 
# They are created as part of the deployment process.
def deploy_to_aci(inference_env_name,cpu_cores:int,memory_gb:int,model_name,model_version,deployment_name):
    try:
        inference_config=_create_inference_config(inference_env_name)
    except Exception as e:
        raise e
    try:
        deployment_config=AciWebservice.deploy_configuration(cpu_cores=cpu_cores,memory_gb=memory_gb)
        _start_deploy_model(inference_config,deployment_config,model_name,model_version,deployment_name)
    except Exception as e:
        print("failed to deploy")
        raise e


if __name__ == "__main__":

    # depoly_to_local_web(inference_env_name="confidential_test",
    #                     port_num=6104,
    #                     model_name="dummy_test_model",
    #                     model_version=7,
    #                     deployment_name="dummy-test-deployment")
    deploy_to_aci(inference_env_name="confidential_test_deployment",
                        cpu_cores=1,
                        memory_gb=1,
                        model_name="dummy_test_model",
                        model_version=8,
                        deployment_name="dummy-test-deployment")