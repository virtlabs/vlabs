#!/bin/bash


useradd $SX_U
echo "$SX_P" | passwd --stdin $SX_U


shellinaboxd -t $PARAMS 2>&1
