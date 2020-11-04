import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from  set_up_aml.util import _establish_connection_to_aml_workspace
import torch

def upload_file(path_to_local_file,path_to_blob):
    try:
        ws=_establish_connection_to_aml_workspace()
    except Exception as e:
        print("failed to connect to worksapce")
        raise e
    try:
        default_data_store=ws.get_default_datastore()
        default_data_store.upload_files(files=path_to_local_file,
        target_path=path_to_blob,
        overwrite=True)
    except Exception as e:
        print("failed to upload")
        raise e

if __name__ == "__main__":
    try:
        dummy_data=torch.randn(256,10)
        torch.save(dummy_data,'dummy_data_file')
        upload_file(["dummy_data_file"],"dummy")
    except Exception as e:
        print(e)