# Reserving the machines
```
	./reserve.sh
	./deploy.sh
```

# Setting up the Kubernetes cluster
```	
	./prepare.sh
```

# Launching the cluster
	
	ssh root@[MASTER_NODE]
	kubeadm init --config kubeadm-config.yaml

	In the output of `kubeadm init` there will be a kubeadm join command, launch it on every desired worker node
	For example:
	ssh root@[WORKER_NODE]
	kubeadm join 172.16.52.5:6443 --token [TOKEN] \
	--discovery-token-ca-cert-hash sha256:[SHA256_HASH]

# Network add-on for Kubernetes
	Here we'll use Weave, but another one can be used.
```	 
	export KUBECONFIG=/etc/kubernetes/admin.conf
	kubectl apply -f https://github.com/weaveworks/weave/releases/download/v2.8.1/weave-daemonset-k8s.yaml
```

# Monitoring

```
./setup_monitoring.sh
```

# TeaStore

	```
	./teastore.sh
	kubectl create -f teastore-clusterip.yaml
	```

# Load generation

	```
		./generate_dataset.sh conf/teastore.conf 
	```

# HPA

	```
		kubectl apply -f components.yaml
		kubectl create -f hpa.yaml
	```
