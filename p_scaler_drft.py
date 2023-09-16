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
import math
import time
import argparse
import requests
from datetime import datetime, timedelta
from kubernetes import client, config
DEPLOYMENTS = ["teastore-webui", "teastore-persistence", "teastore-auth", "teastore-recommender", "teastore-image"]
DEPLOYMENT_NAME = "teastore-webui"
CPU=0.7
MAX_PRESSURE = 0.2
PROMETHEUS_IP = ""
TEASTORE_URL = "172.16.52.8:9100"
PROMETHEUS_URL = "http://172.16.52.9:30090"


def cpu_convert(val):
    if "n" in val:
        val = val.strip("n")
        return int(val)*1e-9
    elif "u" in val:
        val = val.strip("u")
        return int(val)*1e-6
    

def update_deployment(api, deployment, replicas, name):
    # Update container image
    deployment.spec.replicas = replicas

    # patch the deployment
    resp = api.patch_namespaced_deployment(
        name=name, namespace="default", body=deployment
    )

    print("\n[INFO] deployment's container image updated.\n")
    print("%s\t%s\t\t\t%s" % ("NAMESPACE", "NAME", "replicas"))
    print(
        "%s\t\t%s\t\t\t%s\n"
        % (
            resp.metadata.namespace,
            resp.metadata.name,
            resp.spec.replicas,
        )
    )


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    parser = argparse.ArgumentParser(description='')
    # parser.add_argument('-r', '--replicas', default=2, help='number of replicas')

    args = parser.parse_args()

    config.load_kube_config()

    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    custom_api = client.CustomObjectsApi()

    # # print(k8s_nodes.items)
    # for stats in k8s_nodes['items']:
    #     print("Node Name: %s\tCPU: %s\tMemory: %s" % (stats['metadata']['name'], stats['usage']['cpu'], stats['usage']['memory']))

    # print("Listing pods with their IPs:")
    # ret = v1.list_pod_for_all_namespaces(watch=False)
    # for i in ret.items:
    #     print("%s\t%s\t%s" %
    #           (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    nodes = []
    # node = custom_api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes", field_selector="metadata.name=" + pods.items[0].spec.node_name)

    # url = prometheus_url + '/api/v1/query?'
    url = prometheus_url + '/api/v1/query_range?'

    while True:
        MAX_CPU = 0.7
        payload = {'query': "rate(node_pressure_cpu_waiting_seconds_total{instance='"+ TEASTORE_URL +"'}[60s])", 'start': (datetime.now()-timedelta(seconds=10)).timestamp(), 'end': datetime.now().timestamp(), 'step': '1s'}
        payload_mem = {'query': "rate(node_pressure_memory_waiting_seconds_total{instance='"+ TEASTORE_URL +"'}[60s])", 'start': (datetime.now()-timedelta(seconds=10)).timestamp(), 'end': datetime.now().timestamp(), 'step': '1s'}

        cpu_pressure = 0
        mem_pressure = 0

        try: 
            res = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload).json()
            mem_res = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload_mem).json()

            cpu_pressures = 0
            mem_pressures = 0

            for val in res["data"]["result"][0]["values"]:
                cpu_pressures += float(val[1])

            for val in mem_res["data"]["result"][0]["values"]:
                mem_pressures += float(val[1])

            cpu_pressure = cpu_pressures/len(res["data"]["result"][0]["values"])
            mem_pressure = mem_pressures/len(mem_res["data"]["result"][0]["values"])

        except Exception as e:
            print(e)
            cpu_pressure = MAX_PRESSURE
            mem_pressure = 1

        print("#####################")
        print("pressure ", cpu_pressure)        
        print("memory pressure ", mem_pressure)
        down =False
        if mem_pressure > 0: #cpu_pressure > MAX_PRESSURE or
            down = True
            # time.sleep(5)
            # continue
            MAX_CPU = 0.8
            print("downscale")

        for dep_name in DEPLOYMENTS:
            pods = v1.list_namespaced_pod("default", label_selector="run=" + dep_name, field_selector="status.phase=Running")
            # import ipdb
            # ipdb.set_trace()
            cpus = []
            print(dep_name)
            for pod in pods.items:
                info = custom_api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods", field_selector="metadata.name=" + pod.metadata.name)
                # payload = {'query': 'container_cpu_usage_seconds_total{pod="' + pod.metadata.name + '", metrics_path="/metrics/resource"}', 'time': datetime.now().timestamp()}
                # payload_2 = {'query': 'container_cpu_usage_seconds_total{pod="' + pod.metadata.name + '", metrics_path="/metrics/resource"}', 'time': (datetime.now()-timedelta(seconds=20)).timestamp()}
                # #payload_3 = {'query': 'kube_pod_status_ready{pod="' + pod.metadata.name + '"}', 'time': datetime.now().timestamp()}

                # res = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload).json()
                # res_2 = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload_2).json()
                #res_3 = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=payload_2).json()

                if not info and not info['items'] and not info['items'][0]['containers']:
                    print("no res")
                    continue
                # print(res)
                # print(res_2)
                # cpu_1 = float(res["data"]["result"][0]["value"][1])
                # cpu_2 = float(res_2["data"]["result"][0]["value"][1])
                #n_pods = res_3["data"]["result"][0]["value"][1]

                # g_cpu = cpu_1 - cpu_2
                g_cpu = 0
                try:
                    g_cpu = cpu_convert(info['items'][0]['containers'][0]['usage']['cpu'])
                except Exception as e:
                    print(e)
                    continue

                if g_cpu:
                    cpus.append(g_cpu)
                    print("cpu ", g_cpu)
            
            n_pods = len(pods.items)
            avg_cpu = sum(cpus)/n_pods 

            # if down:
            if True:
                print("sum method")
                sum_cpu = sum(cpus) 
                print("max cpu", MAX_CPU)
                new_pods = max(math.ceil(sum_cpu/MAX_CPU), 1)
            # else:
            #     print("avg method")
            #     new_pods = math.ceil(n_pods*avg_cpu/MAX_CPU)

            print("avg cpu ", avg_cpu)
            print("prev pods", n_pods)
            print("new pods", new_pods)

            #if new_pods > 10:
            new_pods = min(10, new_pods)

            if mem_pressure >= 0.1:
                new_pods = 1

            if n_pods!=new_pods: #avg_cpu >= MAX_CPU:
                deployment = apps_v1.read_namespaced_deployment(name=dep_name, namespace='default')
                print("scale ", dep_name)

                if down and n_pods < new_pods:
                    print("No upscaling")
                    continue
                
                update_deployment(apps_v1, deployment, new_pods, dep_name)

        time.sleep(10)


if __name__ == '__main__':
    main()
