#!/bin/bash
ENDPOINT=http://192.168.0.112:8080
SFILE=bigfile1
DFILE=s3://am-snowball1/bigfile6
aws s3 cp ${SFILE} ${DFILE} \
  --profile snowballEdge \
  --endpoint ${ENDPOINT}
