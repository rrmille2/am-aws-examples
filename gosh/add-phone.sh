#!/bin/bash

export AWS_PROFILE=gosh

aws dynamodb put-item \
  --table-name SALaunchPhones  \
  --item "{ \"PhoneNumber\": {\"S\": \"${1}\"}  }" \
  --return-consumed-capacity TOTAL  

