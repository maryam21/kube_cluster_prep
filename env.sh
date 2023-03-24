#!/bin/bash

export USERNAME=mahhttouche
export DIR=/home/$USERNAME && export NODES_FILE=$DIR/kube_cluster_prep/nodesfile && export N_HOSTS=3 && \
export PERIOD=4 && export CLUSTER_NAME=nova && export MASTER_NODE=$(head -n 1 $NODES_FILE) && \
export PROM_NODE=$(tail -1 $NODES_FILE)
