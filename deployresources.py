from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

def create_or_update_resource_group():
    # Define your Azure subscription ID and resource group name
    subscription_id = "4474a5f6-6fe7-4001-94b7-5dc9206a07f4"
    resource_group_name = "lab4"
    location = "westeurope"  

    # Create a DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Create a ResourceManagementClient instance
    client = ResourceManagementClient(credential, subscription_id)

    # Define the resource group parameters
    parameters = {"location": location}

    # Create or update the resource group
    result = client.resource_groups.create_or_update(resource_group_name, parameters)
    print(f"Resource group creation/update status: {result}\n\n")

def create_virtual_network():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="4474a5f6-6fe7-4001-94b7-5dc9206a07f4",
    )

    response = client.virtual_networks.begin_create_or_update(
        resource_group_name="lab4",
        virtual_network_name="net4",
        parameters={
            "location": "westeurope",
            "properties": {"addressSpace": {"addressPrefixes": ["10.0.0.0/16"]}, "flowTimeoutInMinutes": 10},
        },
    ).result()
    print(f"Sucessfully created virtual network: {response}\n\n")

def create_subnet():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="4474a5f6-6fe7-4001-94b7-5dc9206a07f4",
    )

    response = client.subnets.begin_create_or_update(
        resource_group_name="lab4",
        virtual_network_name="net4",
        subnet_name="snet4",
        subnet_parameters={"properties": {"addressPrefix": "10.0.0.0/16"}},
    ).result()
    print(f"Sucessfully created subnet {response}\n\n")

def create_public_ip_address():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="4474a5f6-6fe7-4001-94b7-5dc9206a07f4",
    )

    response = client.public_ip_addresses.begin_create_or_update(
        resource_group_name="lab4",
        public_ip_address_name="ip4",
        parameters={"location": "westeurope"},
    ).result()
    print(f"Sucessfully created IP address {response}\n\n")

def create_network_interface():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="4474a5f6-6fe7-4001-94b7-5dc9206a07f4",
    )

    try:
        response = client.network_interfaces.begin_create_or_update(
            resource_group_name="lab4",
            network_interface_name="nic4",
            parameters={
                "location": "westeurope",
                "properties": {
                    #"disableTcpStateTracking": True,
                    "enableAcceleratedNetworking": True,
                    "ipConfigurations": [
                        {
                            "name": "ip4",
                            "properties": {
                                "publicIPAddress": {
                                    "id": "/subscriptions/4474a5f6-6fe7-4001-94b7-5dc9206a07f4/resourceGroups/lab4/providers/Microsoft.Network/publicIPAddresses/ip4"
                                },
                                "subnet": {
                                    "id": "/subscriptions/4474a5f6-6fe7-4001-94b7-5dc9206a07f4/resourceGroups/lab4/providers/Microsoft.Network/virtualNetworks/net4/subnets/snet4"
                                },
                            },
                        }
                    ],
                },
            },
        ).result()
        print(f"Sucessfully created network interface: {response}\n\n")
    except Exception as e:
        print(f"Error creating network interface: {e}")

def create_virtual_machine():
    # Define your Azure subscription ID and resource group name
    subscription_id = "4474a5f6-6fe7-4001-94b7-5dc9206a07f4"
    resource_group_name = "lab4"
    location = "westeurope"  # Replace with the desired location

    # Create a DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Create ComputeManagementClient and NetworkManagementClient instances
    compute_client = ComputeManagementClient(credential, subscription_id)
    network_client = NetworkManagementClient(credential, subscription_id)

    # Define VM configuration
    vm_name = "vm4"
    admin_username = "omoni"
    ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCtOG/v4tzMH+TOPysWoakehRQ7YGqlUYekqUJXSMW+/uzanq1RBQ1gyXlHv0M+f8+xPwTjcsoQfsz5f2ciLnoGBUuqmAMxK1hYkE5WALb0mLomhirum7CI+lS51AG4FjXf2ks7sxdvoKJibfvKDSDHvfMS6pDwNLYtkFeFm7aQE751HRET9yTcWqDzcKk9fxZZ00ZCAufXv0YP+z/MlP4pGZGRYCaZtWmjI3XTeMiIg3/tkQfduIh97nsmV/qbUN27MexWq6YbfQdkaAqAi6+1RF5UpfJIgpJnf78D/TA6MgP+9O+AQNx08ZS8Xj8yQq9lxIT6Qv1t4zVAtIoYwKrgMsU2C8b13YFRGyMmVnR6mjg2eMmlJi33WqeVIMGq0KvVBROhftUFFpy/z0mDaPHuUSlaspunXIKXcPv74F5bNDtBzxIYo+8vbvxXYPbxqgjNR+nL83rYBgCD3EINIkf7NeQoEBYbGRBpcgZFYKBEjdF+EZZDIVUrb+1ghX2zvn8= omoni@LAPTOP-2NJ9QU8E"
    vm_size = "Standard_D1_v2"

    # Define the virtual machine properties
    vm_properties = {
        "location": location,
        "osProfile": {
            "adminUsername": admin_username,
            "secrets": [],
            "computerName": vm_name,
            "linuxConfiguration": {
                "ssh": {
                    "publicKeys": [
                        {
                            "path": "/home/omoni/.ssh/authorized_keys",
                            "keyData": ssh_public_key
                        }
                    ]
                },
                "disablePasswordAuthentication": True
            }
        },
        "networkProfile": {
            "networkInterfaces": [
                {
                    "id": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkInterfaces/nic4",
                    "properties": {
                        "primary": True
                    }
                }
            ]
        },
        "storageProfile": {
            "imageReference": {
                "sku": "16.04-LTS",
                "publisher": "Canonical",
                "version": "latest",
                "offer": "UbuntuServer"
            },
            "dataDisks": []
        },
        "hardwareProfile": {
            "vmSize": vm_size
        },
        "provisioningState": "Creating"
    }

    # Create the virtual machine
    vm = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name, vm_name, vm_properties)
    vm.wait()
    print("Successfully created VM!\n")
    print(vm.result())

    

if __name__ == "__main__":
    create_or_update_resource_group()
    create_virtual_network()
    create_subnet()
    create_public_ip_address()
    create_network_interface()
    create_virtual_machine()