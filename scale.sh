#!/bin/bash

source $DIR/env.sh

kubectl scale --replicas=2 deployment/teastore-webui deployment/teastore-persistence && start=$(date) && echo $start
# 03:42:46  web=13:42:48,  pers=13:42:48
#1688463769  end=1688463772 - 3s 

kubectl scale --replicas=2 deployment/teastore-webui && kubectl scale --replicas=2 deployment/teastore-persistence && start=$(date) && echo $start
#03:46:54 web=13:46:56  pers=13:46:56
#1688463851 end=1688463853 - 2s
#script: 2023-07-06 10:05:51.349163  scale= 08:05:53

## 3
kubectl scale --replicas=2 deployment/teastore-webui deployment/teastore-persistence deployment/teastore-db && start=$(date) && echo $start
#03:52:11  13:52:13  13:52:12  13:52:12

kubectl scale --replicas=2 deployment/teastore-webui && kubectl scale --replicas=2 deployment/teastore-persistence && kubectl scale --replicas=2 deployment/teastore-db && start=$(date) && echo $start
#03:55:34  13:55:36  
#script: 10:12:30.831424  08:12:32 

## 4
kubectl scale --replicas=2 deployment/teastore-webui deployment/teastore-persistence deployment/teastore-db deployment/teastore-recommender && start=$(date) && echo $start
#04:12:45   14:12:47   14:12:46  ...

kubectl scale --replicas=2 deployment/teastore-webui && kubectl scale --replicas=2 deployment/teastore-persistence && kubectl scale --replicas=2 deployment/teastore-db && kubectl scale --replicas=2 deployment/teastore-recommender && start=$(date) && echo $start
# 04:17:19   14:17:21  

## 5
kubectl scale --replicas=2 deployment/teastore-webui deployment/teastore-persistence deployment/teastore-db deployment/teastore-recommender deployment/teastore-image && start=$(date) && echo $start
#04:23:27 14:23:29

kubectl scale --replicas=2 deployment/teastore-webui && kubectl scale --replicas=2 deployment/teastore-persistence && kubectl scale --replicas=2 deployment/teastore-db && kubectl scale --replicas=2 deployment/teastore-recommender && kubectl scale --replicas=2 deployment/teastore-image && start=$(date) && echo $start
# 04:47:37  14:47:39   rec,img=14:47:40

kubectl get pod "teastore-db-56fcd8fcdd-txf6l" -o json | jq ".status.conditions[] | select(.type == \"Ready\" and .status == \"True\") | .lastTransitionTime" | tr -d '"'

kubectl scale --replicas=1 deployment/teastore-webui deployment/teastore-persistence deployment/teastore-db deployment/teastore-recommender deployment/teastore-image 

#