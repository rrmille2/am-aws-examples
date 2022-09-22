# after the snowball edge is powered on, see if the device is accessible
./do-snowball.sh describe-device

# now unlock the snowball edge
./do-snowball.sh unlock-device

# and now you can use s3 commands to access the device
# in this example, list the buckets
aws s3 ls --profile snowballEdge --endpoint http://192.168.0.112:8080


