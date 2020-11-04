from threading import main_thread
from azureml.core import Workspace
from azureml.core.compute import ComputeTarget, RemoteCompute,AmlCompute
from azureml.core.compute_target import ComputeTargetException
from util import _establish_connection_to_aml_workspace,_get_compute_target

def create_compute_instance():
    try:
        ws=_establish_connection_to_aml_workspace()
    except Exception as e:
        raise e
    try:
        compute_target_name='testConfDSVM'
        attach_config=RemoteCompute.attach_configuration(
            # resource_id="/subscriptions/e4da59ca-11b0-454e-a89a-cd711dea9094/resourceGroups/Barrys-ConfidentialML-Test/providers/Microsoft.Compute/virtualMachines/Barrys-ConfidentialML-TestComputeTarget",
            resource_id="/subscriptions/e4da59ca-11b0-454e-a89a-cd711dea9094/resourcegroups/Barrys-ConfidentialML-Test/providers/Microsoft.Compute/virtualMachines/BarrysTestConfidentialDSVM",
            ssh_port=22,
            username="barryzhang",
            password="123456789Abc"
        )
        compute=ComputeTarget.attach(ws,compute_target_name,attach_config)
        compute.wait_for_completion(show_output=True)
    except Exception as e:
        raise e

def create_compute_cluster():
    try:
        print("Start searching for user's compute target...")
        ws=_establish_connection_to_aml_workspace()
    except Exception as e:
        raise e
    try:
        compute_target = _get_compute_target(ws,"StandardCompute")
        print("User already has a compute target!")
    except ComputeTargetException:
        print("User does not have a compute target, starts creating...")
        compute_config = AmlCompute.provisioning_configuration(vm_size="Standard_F4s_v2",
                                                                max_nodes=4, 
                                                                idle_seconds_before_scaledown=2400)
        cpu_cluster = ComputeTarget.create(ws, "StandardCompute", compute_config)
        cpu_cluster.wait_for_completion(show_output=True)
        print("compute target craeted!")
    except Exception as e:
        raise e

if __name__ == "__main__":
    try:
        create_compute_instance()
        # create_compute_cluster()
        print("Succeeded!")
    except Exception as e:
        print("failed due to {}".format(e))



