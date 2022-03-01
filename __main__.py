"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import boto3

# interface class
class ImportVMSeeder:
    # identifier that the api_handle uses for the VM
    # instance ID for AWS (eg i-03da53f68741b833b)
    # resource_id for Azure (eg /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.Compute/virtualMachines/machine1)
    vm_handle: str

    # handle for the VM within Pulumi's state
    name: str

    # string representation of the provider. not sure why I'd want this but just in case
    cloud_provider: str

    # dependency inversion
    api_handle = None

    def __init__(self, vm_handle: str, name: str, api_handle) -> None:
        # do the lookups in the constructor so that the caller can just access the relevant attributes
        # if the caller wants the whole lot of values, it can call the get member function to get them in a dict
        ...

    def get_object(self) -> dict:
        ...


# concrete implementation for AWS instances
class ImportAWSVMSeeder(ImportVMSeeder):
    instance_object = None  #: boto3.resources.factory.ec2.Instance
    ami: str
    instance_type: str

    def __init__(self, vm_handle: str, name: str, api_handle) -> None:
        self.name = name
        self.cloud_provider = "AWS"
        self.api_handle = api_handle
        self.vm_handle = vm_handle
        self.instance_object = api_handle.Instance(id=vm_handle)
        self.ami = self.instance_object.image_id
        self.instance_type = self.instance_object.instance_type
        # security_groups=[group.name]

    def get_object(self) -> dict:
        return {
            "name": self.name,
            "ami": self.ami,
            "instance_type": self.instance_type,
            "vm_handle": self.vm_handle,
        }


# concrete implementation for Azure instances
# todo: do this when I next work with Azure stuff...
class ImportAWSVMSeeder(ImportVMSeeder):
    # Azure VM specific stuff goes here
    # Subsription, Resource Group etc

    def __init__(self, vm_handle: str, name: str, api_handle) -> None:
        self.name = name
        self.cloud_provider = "Azure"
        self.api_handle = api_handle
        self.vm_handle = vm_handle
        # self.instance_object = api_handle.Instance(id=vm_handle)
        # security_groups=[group.name]

    def get_object(self) -> dict:
        ...


# EXAMPLE USAGE:
# set up aws api
ec2_api = boto3.resource("ec2")

# instantiate the importer helper
importer = ImportAWSVMSeeder(
    vm_handle="i-03da53f68741b833b", name="jripper", api_handle=ec2_api
)

# do the import
server = aws.ec2.Instance(
    importer.name,
    ami=importer.ami,
    instance_type=importer.instance_type,
    opts=pulumi.ResourceOptions(import_=importer.vm_handle),
)

# done, its now in Pulumi's state
