import boto3
import sys
import argparse
import time
import botocore
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('--region', default='us-east-1')
parser.add_argument('--db-id', required=True) # RDS name
parser.add_argument('--storage', default=100)
parser.add_argument('--db-name', type=str, default='service')
parser.add_argument('--engine', type=str, default='postgres')
parser.add_argument('--storage-type', type=str, default='gp2')
parser.add_argument('--master-user-name', type=str, default='mypassword')
parser.add_argument('--master-user-password', type=str, default='mypassword')
parser.add_argument('--db-instance-class', type=str, default='db.t2.small')
parser.add_argument('--wait-for', type=int, default=60,
                    help='Wait for N minutes')
args = parser.parse_args()
print(args)

rds_client = boto3.client('rds', region_name=args.region)

def create_rds_instance(rds_name):
    db_subnet_group = 'default'
    try:
        rds_client.create_db_instance(DBInstanceIdentifier=rds_name,
                            AllocatedStorage=args.storage,
                            DBName=args.db_name,
                            Engine=args.engine,
                            StorageType=args.storage_type,
                            StorageEncrypted=False,
                            MultiAZ=False,
                            MasterUsername=args.master_user_name,
                            MasterUserPassword=args.master_user_password,
                            VpcSecurityGroupIds=['default'],
                            DBInstanceClass=args.db_instance_class,
                            PubliclyAccessible=False,
                            DBSubnetGroupName=db_subnet_group,
                            Tags=[{'Key': 'Name', 'Value': args.stack_name + '-SERVICE'}])
        print('Starting RDS instance with ID:{}'.format(rds_name))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'DBInstanceAlreadyExists':
            print("RDS Instance {} already exists\nUse  a different name for RDS Instance".format(args.db_id))
            exit(1)

    waiter = rds_client.get_waiter('db_instance_available').wait(DBInstanceIdentifier=rds_name)
    response = rds_client.describe_db_instances(DBInstanceIdentifier=rds_name)
    host = response['DBInstances'][0]['Endpoint']['Address']
    print('DB instance ready with host:{}'.format(host))
    return host
