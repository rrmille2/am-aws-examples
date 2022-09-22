## AutoStop 

Automatically stop SageMaker Notebook Instances if the quantity of instances (of a particular instance type) reaches a pre-defined maximum.

Here are the steps to setup the AWS resources:

1. Create a new Role and Permissions
This Role will be used by the Lambda function created in the next step.

Create a Role with the following Trust Relationship:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```


For this new Role, create an inline Policy with the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sagemaker:*"
            ],
            "Resource": "*"
        }
    ]
}
```

2. Create the Lambda function 
Specify the following parameters:
a. Python 3.8 or later
b. Use the Role created in the previous step.

Copy and paste the `lambda.py` code into your Lambda function. Be sure to save and Deploy.


1. Create An EventBridge Rule
The Rule is triggered on the event "SageMaker Notebook Instance State Change". When this Rule is triggered, it invokes the Lambda function created in the previous step.

Use the following Event Pattern when creating the Rule:

```json
{
  "source": ["aws.sagemaker"],
  "detail-type": ["SageMaker Notebook Instance State Change", "SageMaker Endpoint State Change"]
}
```

Specify the Lambda function created above as the target for this Rule.


