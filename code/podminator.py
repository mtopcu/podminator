from kubernetes import client, config

def main():
        
    try:
        config.load_kube_config()
    except config.ConfigException:
        raise Exception("Could not configure kubernetes python client!")

    app_v1 = client.AppsV1Api()
    replica_sets = app_v1.list_namespaced_replica_set(namespace="default")
    replica_set_names = [i.metadata.name for i in replica_sets.items]
    
    if not replica_set_names:
        print('\nThere is not any pod which belongs to any Replica Set!\n')
        return

    core_v1 = client.CoreV1Api()
    pods = core_v1.list_namespaced_pod(namespace="default")
    pod_names = [i.metadata.name for i in pods.items]
    
    killing_pods = list() 

    for replica_set in replica_set_names:

        killing_pods = [pod_name for pod_name in pod_names if replica_set in pod_name]
        mid_index = len(killing_pods)//2
        
        for pod in killing_pods[:mid_index]:
            core_v1.delete_namespaced_pod(name=pod,
                namespace="default",
                body=client.V1DeleteOptions())
        
        killing_pods = list()

    pod_number = len(pod_names)
    print("\n" + "─" * 62)
    print(f' There were {pod_number} pods and {pod_number//2} of the them have been TERMINATED!')
    print("─" * 62 + "\n")

if __name__ == "__main__":
    main()
