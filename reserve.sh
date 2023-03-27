#!/bin/bash

source env.sh && \
oarsub -I -p $CLUSTER_NAME -l host=$N_HOSTS,walltime=$PERIOD  -t deploy

