# Copyright 2016 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Shows how to load a Kubernetes config from outside of the cluster.
https://github.com/kubernetes-client/python
"""
import time
from datetime import datetime 

from kubernetes import client, config

DEPLOYMENTS = ["teastore-webui", "teastore-persistence", "teastore-image", "teastore-auth"]    

def update_deployment(api, deployment, replicas, name):
    # Update container image
    deployment.spec.replicas = replicas

    # patch the deployment
    #start = time.time()
    start = datetime.now() 
    resp = api.patch_namespaced_deployment(
        name=name, namespace="default", body=deployment
    )
    print(start)
    # print("\n[INFO] deployment's container image updated.\n")
    # print("%s\t%s\t\t\t%s\t%s" % ("NAMESPACE", "NAME", "REVISION", "IMAGE"))
    # print(
    #     "%s\t\t%s\t%s\t\t%s\n"
    #     % (
    #         resp.metadata.namespace,
    #         resp.metadata.name,
    #         resp.metadata.generation,
    #         resp.spec.replicas,
    #     )
    # )


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    # parser = argparse.ArgumentParser(description='')
    # parser.add_argument('-r', '--replicas', default=2, help='number of replicas')

    # args = parser.parse_args()

    config.load_kube_config()

    apps_v1 = client.AppsV1Api()
    
    for dep_name in DEPLOYMENTS:
        deployment = apps_v1.read_namespaced_deployment(name=dep_name, namespace='default')
        update_deployment(apps_v1, deployment, 2, dep_name)


if __name__ == '__main__':
    main()
