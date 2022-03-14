
########### Importing Required Modules ################

import json
import boto3
import csv

########## Opening a Csv writer and adding headers ##############

csv_writer =  open('export_ec2_data.csv','w')
csv_file = csv.writer(csv_writer)
csv_header = ['regionname','name','instance_id','private_IpAddress','instance_State',
              'instance_Type','status_check','availabiltyZone','public_ip4_dns',
              'public_ipv4_address','monitoring','security_group_name','key_name','launch_time',
              'VolumeId','volume_type','volume_size','snapshot_id','volume_state','volume_iops',
              'attached_instance','subnet_id','vpc_id','Ipv6Addresses']
csv_file.writerow(csv_header)

########### Connecting to Ec2 instances using AWS-SDK(boto3)##########

ec2 = boto3.client('ec2')

############# Fetching all the regions which are present in AWS #########
regions_list = []
regions = ec2.describe_regions()['Regions']
for region in regions:
    regions_list.append(region['RegionName'])
    
############ Fetching the required data using get_ec2_metadata ############

def get_ec2_metadata():
    for region_name in regions_list:
        
        ############connecting to ec2 with region_name ####################
        ec2_client = boto3.client('ec2',region_name)
        ec2_reservations = ec2_client.describe_instances()['Reservations']
        
        ###########connecting to ec2 to get volumes of the instances ###########
        ec2_volumes =boto3.resource('ec2',region_name)
        ec2_volume_instances = ec2_volumes.instances.all()
        
        ##############checking if the length of the reserverations############
        if len(ec2_reservations) == 0:
            print('No ec2 instances avalilable at given {} region '.format(region_name))
        
        ###############if there are any instances at that region will excute the following and fetch the data###########
        else:
            
            ##########Fetching ec2_instances metadata ###########
            
            for reservation in ec2_reservations:
                for instance in reservation['Instances']:
                    if instance.get('Tags') != None:
                        instance_name = instance.get('Tags')[0]['Value']
                    else:
                        instance_name = ''
                    instance_id = instance.get('InstanceId')
                    private_IpAddress = instance.get('PrivateIpAddress')
                    instance_State = instance.get('State')['Name']
                    instance_Type = instance.get('InstanceType')
                    status = instance.get('BlockDeviceMappings')
                    for status in status:
                        status_check = status['Ebs']['Status']
                    availabiltyZone = instance.get('Placement')['AvailabilityZone']
                    public_ip4_dns = instance.get('PublicDnsName')
                    public_ipv4_address = instance.get('PublicIpAddress')
                    monitoring = instance.get('Monitoring')['State']
                    security_groups = instance.get('SecurityGroups')
                    security_group_names = []
                    for security_group in security_groups:
                        security_group_name = security_group['GroupName']
                        security_group_names.append(security_group_name)
                    key_name = instance.get('KeyName')
                    subnet_id = instance.get('SubnetId')
                    vpc_id = instance.get('VpcId')
                    Ipv6Addresses = instance.get('Ipv6Addresses')
                    launch_time = instance.get('LaunchTime')
                    volume_ids = instance.get('BlockDeviceMappings')
                    for volume in volume_ids:
                        volume_id = volume['Ebs']['VolumeId']
                        
                        
                ########### Fetching ec2 instances volumes data ############   
                for ec2_volumes in ec2_volume_instances:
                    for volume in ec2_volumes.volumes.all():
                        if volume_id == volume.id:
                            volume_id = volume.id
                            volume_type = volume.volume_type
                            volume_size = str(volume.size) + 'GiB'
                            snapshot_id = volume.snapshot_id
                            volume_state = volume.state
                            volume_iops = volume.iops
                            attached_instances = volume.attachments
                            attached_instance=[]
                            for attach_instance in attached_instances:
                                attached_instance.append(attach_instance['InstanceId'])
                        
                ######### Adding the data to required feilds in csv format ###########
                
                csv_data = [region_name,instance_name,instance_id,private_IpAddress,instance_State,
                            instance_Type,status_check,availabiltyZone,public_ip4_dns,
                            public_ipv4_address,monitoring,security_group_names,key_name,
                            launch_time,volume_id,volume_type,volume_size,snapshot_id,
                            volume_state,volume_iops,attached_instance,subnet_id,vpc_id,Ipv6Addresses]
                csv_file.writerow(csv_data)

get_ec2_metadata()