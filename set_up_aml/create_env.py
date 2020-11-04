from azureml.core import Workspace, Environment
from util import _establish_connection_to_aml_workspace

def register_new_conda_environment(env_name):
    try:
        ws=_establish_connection_to_aml_workspace()
    except Exception as e:
        raise e
    try:
        new_env=Environment.from_conda_specification(name=env_name,
        file_path=r'set_up_aml\test_env.yml')
        new_env.register(ws)
        print("New environment {} has been registerd".format(env_name))
    except Exception as e:
        raise e

def show_list_of_all_environments():
    try:
        ws=_establish_connection_to_aml_workspace()
    except Exception as e:
        raise e
    try:
        env_list=Environment.list(ws)
        for key in env_list:
            print(key)
    except Exception as e:
        raise e

def show_list_of_all_custom_environments():
    try:
        ws=_establish_connection_to_aml_workspace()
    except Exception as e:
        raise e
    try:    
        env_list=Environment.list(ws)
        for key in env_list:
            if('AzureML' not in key):
                print(key)
    except Exception as e:
        raise e

def get_custom_env(env_name):
    try:
        ws=_establish_connection_to_aml_workspace()
    except Exception as e:
        raise e
    try:
        new_env=Environment.get(ws,env_name)
        return new_env
    except Exception as e:
        raise e

if __name__ == "__main__":
    # register_new_conda_environment("confidential_test")
    show_list_of_all_custom_environments()
