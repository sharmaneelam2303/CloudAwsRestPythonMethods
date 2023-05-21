import boto3
from botocore.exceptions import ClientError

aws_access_key_id = "some_ws_access_key_id"
aws_secret_access_key = "some_aws_secret_access_key"

ec2client = boto3.client(
    "ec2",
    region_name="us-west-2",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)
iamClient = boto3.client(
    "iam",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)
s3Client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)


def __getTotalCountForAwsAutoScalingGroups():
    total = 0
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        autoscaling = boto3.client(
            "autoscaling",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        groups = autoscaling.describe_auto_scaling_groups()
        regCount = 0
        for _ in groups["AutoScalingGroups"]:
            regCount = regCount + 1
            total = total + 1
    return total


def __getTotalCountForAwsEbsVolume():
    total = 0
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        ec2 = boto3.client(
            "ec2",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        network = ec2.describe_volumes()
        regCount = 0
        for _ in network["Volumes"]:
            regCount = regCount + 1
            total = total + 1
    return total


def __getTotalCountForAwsIamUser():
    total = 0
    marker = None
    while True:
        paginator = iamClient.get_paginator("list_users")
        response_iterator = paginator.paginate(
            PaginationConfig={"PageSize": 1000, "StartingToken": marker}
        )
        for page in response_iterator:
            u = page["Users"]
            for _ in u:
                total = total + 1
        try:
            marker = page["Marker"]
        except KeyError:
            return total


def __getTotalCountForAwsInstances():
    total = 0
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        ec2 = boto3.resource(
            "ec2",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        for _ in ec2.instances.all():
            total = total + 1
    return total


def __getTotalCountForAwsInternetGateway():
    total = 0
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        ec2 = boto3.client(
            "ec2",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        gateways = ec2.describe_internet_gateways()
        for _ in gateways["InternetGateways"]:
            total = total + 1
    return total


def __getTotalCountForAwsLambdaFunction():
    total = 0
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        lambdaClient = boto3.client(
            "lambda",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        try:
            functions = lambdaClient.list_functions()
            regCount = 0
            for _ in functions["Functions"]:
                regCount = regCount + 1
                total = total + 1
        except ClientError:
            print("Region : {} : Lambda is not available in this region".format(reg))
    return total


def __getTotalCountForAwsLoadBalancer():
    elbv2total = 0
    elbtotal = 0
    ec2client = boto3.client(
        "ec2",
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        client = boto3.client(
            "elbv2",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        response = client.describe_load_balancers()
        for _ in response["LoadBalancers"]:
            elbv2total = elbv2total + 1
        client = boto3.client(
            "elb",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        response = client.describe_load_balancers()
        for _ in response["LoadBalancerDescriptions"]:
            elbtotal = elbtotal + 1
    return elbtotal + elbv2total


def __getTotalCountForAwsNetworkAcl():
    total = 0
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        ec2 = boto3.client(
            "ec2",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        network = ec2.describe_network_acls()
        regCount = 0
        for _ in network["NetworkAcls"]:
            regCount = regCount + 1
            total = total + 1
    return total


def __getTotalCountForAwsRds():
    total = 0
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        rdsClient = boto3.client(
            "rds",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        dbs = rdsClient.describe_db_instances()
        for _ in dbs["DBInstances"]:
            total = total + 1
    return total


def __getTotalCountForAwsRouteTables():
    total = 0
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        ec2 = boto3.client(
            "ec2",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        route = ec2.describe_route_tables()
        regCount = 0
        for _ in route["RouteTables"]:
            regCount = regCount + 1
            total = total + 1
    return total


def __getTotalCountForAwsS3Buckets():
    total = 0
    buckets = s3Client.list_buckets()
    for _ in buckets["Buckets"]:
        total = total + 1
    return total


def __getTotalCountForAwsSecurityGroup():
    total = 0
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        ec2 = boto3.client(
            "ec2",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        security = ec2.describe_security_groups()
        regCount = 0
        for _ in security["SecurityGroups"]:
            regCount = regCount + 1
            total = total + 1
    return total


def __getTotalCountForAwsSubnet():
    total = 0
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        ec2 = boto3.client(
            "ec2",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        subnets = ec2.describe_subnets()
        for _ in subnets["Subnets"]:
            total = total + 1
    return total


def __getTotalCountForAwsVpc():
    total = 0
    for region in ec2client.describe_regions()["Regions"]:
        reg = region["RegionName"]
        ec2 = boto3.client(
            "ec2",
            region_name=reg,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        vpcs = ec2.describe_vpcs()
        for _ in vpcs["Vpcs"]:
            total = total + 1
    return total


def getAwsTotalCountOfResource(resourceName):
    if resourceName == "Instance":
        total = __getTotalCountForAwsInstances()
    elif resourceName == "VPC":
        total = __getTotalCountForAwsVpc()
    elif resourceName == "IAM User":
        total = __getTotalCountForAwsIamUser()
    elif resourceName == "RDS":
        total = __getTotalCountForAwsRds()
    elif resourceName == "Subnet":
        total = __getTotalCountForAwsSubnet()
    elif resourceName == "Security Group":
        total = __getTotalCountForAwsSecurityGroup()
    elif resourceName == "Route Table":
        total = __getTotalCountForAwsRouteTables()
    elif resourceName == "Network ACL":
        total = __getTotalCountForAwsNetworkAcl()
    elif resourceName == "S3 Bucket":
        total = __getTotalCountForAwsS3Buckets()
    elif resourceName == "Internet Gateway":
        total = __getTotalCountForAwsInternetGateway()
    elif resourceName == "Auto Scaling Group":
        total = __getTotalCountForAwsAutoScalingGroups()
    elif resourceName == "Load Balancer":
        total = __getTotalCountForAwsLoadBalancer()
    elif resourceName == "EBS Volume":
        total = __getTotalCountForAwsEbsVolume()
    elif resourceName == "Lambda Function":
        total = __getTotalCountForAwsLambdaFunction()
    else:
        total = 0
    return total
