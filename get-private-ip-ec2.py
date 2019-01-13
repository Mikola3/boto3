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
