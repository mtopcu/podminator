from kubernetes import client, config
import logging

def delete_pod(pod, core_v1_api):
    logging.info(f'Terminating pod is {pod}')
    core_v1_api.delete_namespaced_pod(name=pod,
                namespace="default",
                body=client.V1DeleteOptions())


def print_result(pods):
    pod_number = len(pods)
    print("─" * 82)
    print(f' There are {pod_number} pods on the Replica Sets and {pod_number//2} of the them have been TERMINATED!')
    print("─" * 82 + "\n")


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    try:
        config.load_kube_config()
    except config.ConfigException:
        logging.error("Could not configure kubernetes python client!")

    app_v1_api = client.AppsV1Api()
    replica_sets = app_v1_api.list_namespaced_replica_set(namespace="default")
    replica_set_names = [i.metadata.name for i in replica_sets.items]

    if not replica_set_names:
        logging.warning('There is not any pod which belongs to any Replica Set!')
        return

    core_v1_api = client.CoreV1Api()
    pods = core_v1_api.list_namespaced_pod(namespace="default")
    pod_names = [i.metadata.name for i in pods.items]

    replica_set_pods = [pod for pod in pod_names if any(map(lambda each: each in pod, replica_set_names))]

    killing_pods = list()

    for replica_set in replica_set_names:
        killing_pods = [pod for pod in replica_set_pods if replica_set in pod]
        mid_index = len(killing_pods)//2

        for pod in killing_pods[:mid_index]:
            delete_pod(pod, core_v1_api)

        killing_pods = []

    print_result(replica_set_pods)


if __name__ == "__main__":
    main()
