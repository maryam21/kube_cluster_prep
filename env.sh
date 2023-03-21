#!/bin/bash

export DIR=/home/$USERNAME && export NODES_FILE=$DIR/kube_cluster_prep/nodesfile && export N_HOSTS=3 && \
export PERIOD=8 && export CLUSTER_NAME=sagittaire && export MASTER_NODE=$(head -n 1 $NODES_FILE) && \
export PROM_NODE=$(tail -1 $NODES_FILE)
