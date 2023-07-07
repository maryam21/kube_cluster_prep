#!/bin/bash

export USERNAME=mahhttouche
export DIR=/home/$USERNAME && export NODES_FILE=$DIR/kube_cluster_prep/nodesfile && export N_HOSTS=2 && \
export PERIOD=2 && export CLUSTER_NAME=nova && export MASTER_NODE=$(head -n 1 $NODES_FILE)  && export TEA_NODE=$(head -n 2 $NODES_FILE | sed '2p;d') && \
export PROM_NODE=$(head -3 $NODES_FILE | sed '3p;d') && \
export GENS_FILE=$DIR/metric-dataset-generator/gensfile.txt
export GEN_2=$(tail -2 $NODES_FILE | sed '1p;d') && \
export GEN_1=$(tail -1 $NODES_FILE) && \
export K8S_NODE_IP=172.16.52.$(echo $MASTER_NODE | cut -d . -f 1 | cut -d - -f 2) && export PROM_NODE_IP=172.16.52.$(echo $PROM_NODE | cut -d . -f 1 | cut -d - -f 2) && \
export TEA_NODE_IP=172.16.52.$(echo $TEA_NODE | cut -d . -f 1 | cut -d - -f 2) && export GEN_2_IP=172.16.52.$(echo $GEN_1 | cut -d . -f 1 | cut -d - -f 2) && \
export GEN_1_IP=172.16.52.$(echo $GEN_2 | cut -d . -f 1 | cut -d - -f 2)
