import boto3
import json

aws_access_key_id = 'some_access_key'
aws_secret_access_key = 'some_secret_key'

iamClient = boto3.client('iam', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


role_name = ['role1', 'role2']

policy_arn = ['arn:aws:iam::aws:policy/policy1', 'arn:aws:iam::1234:policy/policy2']

trust_relationship_policy_another_iam_user = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::12344675:root"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "0987654"
                }
            }
        }
    ]
}


def create_role():
    for role in role_name:
        create_role_res = iamClient.create_role(
            RoleName=role,
            AssumeRolePolicyDocument=json.dumps(trust_relationship_policy_another_iam_user),
            Description='This is an automation role',
            Tags=[
                {
                    'Key': 'Owner',
                    'Value': 'Neelam Sharma'
                }
                {
                    'Key': 'Purpose',
                    'Value': 'Testing'
                }
            ]
        )
        print(role, create_role_res)
        for policy in policy_arn:
            policy_attach_res = iamClient.attach_role_policy(
                RoleName=role,
                PolicyArn=policy
            )
            print(policy, policy_attach_res)


create_role()