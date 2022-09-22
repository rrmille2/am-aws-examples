#!/bin/bash

export AWS_PROFILE=gosh

CFID=49f1fbd9-b8f0-4c89-b5d1-9556cda2b912
IID=5db54d7c-252a-4669-a948-9861273b8b9d \
SRC_PNUM="+18327810124"

DST_PNUMS=`aws dynamodb scan --table-name SALaunchPhones | ./phones.py`

DST_PNUMS="8138423093 2062950634 8326475811 2019166260 4254457155 3039192088 3144984485 6469277461 2067654203 6136008510 2532188643 9148046926 7789458135 2158348813 2199283973 6786121391 7039156159 8325457253"
DST_PNUMS="8138423093 2062950634 8326475811 2019166260 4254457155 3039192088"
DST_PNUMS=8138423093 

for DST_PNUM in ${DST_PNUMS}; do

  echo "phone: ${DST_PNUM}"

  aws connect \
    start-outbound-voice-contact \
  --destination-phone-number "+1${DST_PNUM}" \
  --contact-flow-id ${CFID} \
  --instance-id ${IID} \
  --source-phone-number ${SRC_PNUM}

done
