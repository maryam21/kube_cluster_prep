# Reserving the machines
	./reserve.sh
 	./deploy.sh
  	./post_install.sh

# Launching the cluster
	
	 ssh root@[MASTER_NODE]
	 kubeadm init --config kubeadm-config.yaml

	In the output of `kubeadm init` there will be a kubeadm join command, launch it on every desired worker node
	For example:
	 ssh root@[WORKER_NODE]
	 kubeadm join 172.16.52.5:6443 --token [TOKEN] \
	--discovery-token-ca-cert-hash sha256:[SHA256_HASH]

On the master node export:

	 export KUBECONFIG=/etc/kubernetes/admin.conf

# Network add-on for Kubernetes
	Here we'll use Weave, but another one can be used.
	 
	 <!-- kubectl apply -f https://github.com/weaveworks/weave/releases/download/v2.8.1/weave-daemonset-k8s.yaml -->
	 kubectl apply -f weave-daemonset-k8s.yaml
  
  Verify that all nodes are ready with:
  
  	kubectl get nodes
   
Then export the enviroment variables:

   	source env.sh
    
  Make sure "share" folder exists in home directory and local-pvs has the right prometheus node name:
  
	kubectl taint nodes $GEN_1 gens=yes:NoSchedule

# Launch monitoring setup
	
	 ssh root@[MASTER_NODE]
	 source PATH/TO/kube_cluster_prep/setups/setup_env_vars.sh
	 PATH/TO/kube_cluster_prep/setups/setup_monitoring.sh
  
  Verify that all monitoring components are ready:
 	 kubectl get all -n monitoring

# TeaStore setup:
	kubectl create -f teastore-clusterip.yaml
 
 To verify that all pods are running:
	kubectl get pod

# Istio mesh setup

On master node download istio if "istio-1.18.0" folder does not exist:
 

	curl -L https://istio.io/downloadIstio | sh -


	export PATH="$PATH:/root/istio-1.18.0/bin"


	istioctl install -y \
					--set components.egressGateways[0].name=istio-egressgateway \
					--set components.egressGateways[0].enabled=true


	kubectl label namespace default istio-injection=enabled



Create TeaStore pod and the generator pods


	kubectl create -f gen.yaml


then create the gateways:


	kubectl apply -f teastore-gateway.yaml
	kubectl apply -f gen-gateway.yaml


Check that the configuration is correct:

	istioctl analyze

Check the load balancer:


	kubectl get svc istio-ingressgateway -n istio-system


if you have pending status in External IP field then export the following variables:


	export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
	export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')

	export INGRESS_HOST=$(kubectl get po -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].status.hostIP}')

	export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT

	echo "http://$GATEWAY_URL/"


# HPA

	kubectl apply -f components.yaml
	kubectl create -f hpa.yaml
