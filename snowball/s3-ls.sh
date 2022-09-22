#!/bin/bash
ENDPOINT=http://192.168.0.112:8080
SDIR=s3://am-snowball1
aws s3 ls ${SDIR} \
  --profile snowballEdge \
  --endpoint ${ENDPOINT}
