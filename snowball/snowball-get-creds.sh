#!/bin/bash
ENDPOINT=https://192.168.0.112
SBCMD=$1
snowballEdge list-access-keys \
 --manifest-file JIDd8d2447a-0f68-4d4b-8b11-055fa116ab9e_manifest.bin \
 --unlock-code 324f9-5cbb9-7d2f9-259d7-f2e6f \
 --endpoint ${ENDPOINT}

AKEY=T7XLREYRMCFE4M3WX6CD
snowballEdge get-secret-access-key --access-key-id ${AKEY} \
 --manifest-file JIDd8d2447a-0f68-4d4b-8b11-055fa116ab9e_manifest.bin \
 --unlock-code 324f9-5cbb9-7d2f9-259d7-f2e6f \
 --endpoint ${ENDPOINT}

