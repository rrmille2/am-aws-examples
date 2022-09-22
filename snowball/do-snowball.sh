#!/bin/bash
ENDPOINT='https://192.168.0.112'
SBCMD=$1
snowballEdge ${SBCMD} \
 --manifest-file JIDd8d2447a-0f68-4d4b-8b11-055fa116ab9e_manifest.bin \
 --unlock-code 324f9-5cbb9-7d2f9-259d7-f2e6f \
 --endpoint ${ENDPOINT}


