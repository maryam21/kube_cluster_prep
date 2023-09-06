#!/bin/bash

source env.sh
sleep 1
oarsub -I -p $CLUSTER_NAME -l host=$N_HOSTS,walltime=$PERIOD  -t deploy #-t exotic

