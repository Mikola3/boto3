def get_addr(stack_name):
    autoscaling_group_id = cloudformation_client.describe_stack_resource(
        StackName=args.stack,
        LogicalResourceId="AutoScalingGroup"
    )['StackResourceDetail']['PhysicalResourceId']

    # Find ids of instances in autoscaling groups
    instance_id = autoscaling_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[autoscaling_group_id]
    )['AutoScalingGroups'][0]['Instances'][0]['InstanceId']

    return boto3.resource('ec2').Instance(instance_id).private_ip_address

'''
previous hardcode with 5

cloudformation_client = boto3.client('cloudformation', region_name=args.region)
as_group = cloudformation_client.describe_stack_resources(StackName=args.name+'-mystack')['StackResources'][5]['PhysicalResourceId']
print(as_group)

as_client = boto3.client('autoscaling', region_name=args.region)
instance_id = as_client.describe_auto_scaling_groups(AutoScalingGroupNames=[as_group])['AutoScalingGroups'][0]['Instances'][0]['InstanceId']
print(instance_id)

ec2_client = boto3.client('ec2', region_name=args.region)
private_ip = ec2_client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
print(private_ip['PrivateIpAddress'])
'''
