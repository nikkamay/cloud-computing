import requests
import json

subscriptionId = ""
bearer = ""

defaultUrl = f"https://management.azure.com/subscriptions/{subscriptionId}/"

resourceGroupName = "lab7"
virtualNetworkName= "net4"
subnetName= "snet4"
ipName = "ip4"
vmName = "vm4"
apiVersion = "2021-04-01"

def sendHttpRequest(url, json_data, headers):
    # Sending the POST request with the JSON payload
    response = requests.put(url, data=json_data, headers=headers)

    # Checking the answer
    if response.status_code == 200:
        print("Successful request")
        response_data = response.json()
        print("Response data:", response_data)
    else:
        print(f"Print. Statuscode: {response.status_code}")

def createResourceGroup():
    global json_data, headers
    # create Resourcegroup
    urlCreateResourceGroup = f"{defaultUrl}resourcegroups/{resourceGroupName}?api-version={apiVersion}"
    # JSON-Daten
    createResourceGroupPayloadData = {
        "location": "westeurope"
    }
    # Umwandeln der Python-Daten in JSON
    json_data = json.dumps(createResourceGroupPayloadData)
    # Setting the HTTP headers to set the content type to JSON
    headers = {"Authorization": f"Bearer {bearer}",
               'Content-Type': 'application/json'}
    sendHttpRequest(urlCreateResourceGroup, json_data, headers)

def createVirtualNetwork():
    global json_data
    # create virtual network
    urlCreateVirtualNetwork = f"{defaultUrl}resourcegroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}?api-version={apiVersion}"
    payloadDataCreateVirtualNetwork = {
        "properties": {
            "addressSpace": {
                "addressPrefixes": [
                    "10.0.0.0/16"
                ]
            },
            "flowTimeoutInMinutes": 10
        },
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateVirtualNetwork)
    sendHttpRequest(urlCreateVirtualNetwork, json_data, headers)

def createSubnet():
    global json_data
    # create subnet
    urlCreateSubnet = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}?api-version=2023-05-01"
    payloadDataCreateSubnet = {
        "properties": {
            "addressPrefix": "10.0.0.0/16"
        }
    }
    json_data = json.dumps(payloadDataCreateSubnet)
    sendHttpRequest(urlCreateSubnet, json_data, headers)

def createPublicIpAdress():
    global json_data
    # create public ip adress
    urlCreatePublicIPAdress = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/publicIPAddresses/{ipName}?api-version=2023-05-01"
    payloadDataCreatePublicIpAdress = {
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreatePublicIpAdress)
    sendHttpRequest(urlCreatePublicIPAdress, json_data, headers)

def createNetworkInterface():
    global networkInterfaceName, json_data
    # create network interface
    networkInterfaceName = "nic4"
    urlCreateNetworkInterface = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}?api-version=2023-05-01"
    payloadDataCreateNetworkInterface = {
        "properties": {
            "ipConfigurations": [
                {
                    "name": "ipconfig1",
                    "properties": {
                        "publicIPAddress": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/publicIPAddresses/{ipName}"
                        },
                        "subnet": {
                            "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/virtualNetworks/{virtualNetworkName}/subnets/{subnetName}"
                        }
                    }
                }
            ]
        },
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateNetworkInterface)
    sendHttpRequest(urlCreateNetworkInterface, json_data, headers)

def createVm():
    global json_data
    # create VM
    urlCreateVM = f"{defaultUrl}resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}?api-version=2023-07-01"
    payloadDataCreateVM = {
        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Compute/virtualMachines/{vmName}",
        "type": "Microsoft.Compute/virtualMachines",
        "properties": {
            "osProfile": {
                "adminUsername": "omoni",
                "secrets": [

                ],
                "computerName": f"{vmName}",
                "linuxConfiguration": {
                    "ssh": {
                        "publicKeys": [
                            {
                                "path": "/home/omoni/.ssh/authorized_keys",
                                "keyData": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCtOG/v4tzMH+TOPysWoakehRQ7YGqlUYekqUJXSMW+/uzanq1RBQ1gyXlHv0M+f8+xPwTjcsoQfsz5f2ciLnoGBUuqmAMxK1hYkE5WALb0mLomhirum7CI+lS51AG4FjXf2ks7sxdvoKJibfvKDSDHvfMS6pDwNLYtkFeFm7aQE751HRET9yTcWqDzcKk9fxZZ00ZCAufXv0YP+z/MlP4pGZGRYCaZtWmjI3XTeMiIg3/tkQfduIh97nsmV/qbUN27MexWq6YbfQdkaAqAi6+1RF5UpfJIgpJnf78D/TA6MgP+9O+AQNx08ZS8Xj8yQq9lxIT6Qv1t4zVAtIoYwKrgMsU2C8b13YFRGyMmVnR6mjg2eMmlJi33WqeVIMGq0KvVBROhftUFFpy/z0mDaPHuUSlaspunXIKXcPv74F5bNDtBzxIYo+8vbvxXYPbxqgjNR+nL83rYBgCD3EINIkf7NeQoEBYbGRBpcgZFYKBEjdF+EZZDIVUrb+1ghX2zvn8= omoni@LAPTOP-2NJ9QU8E"
                            }
                        ]
                    },
                    "disablePasswordAuthentication": True
                }
            },
            "networkProfile": {
                "networkInterfaces": [
                    {
                        "id": f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/ providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}",
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
                "dataDisks": [

                ]
            },
            "hardwareProfile": {
                "vmSize": "Standard_D1_v2"
            },
            "provisioningState": "Creating"
        },
        "name": f"{vmName}",
        "location": "westeurope"
    }
    json_data = json.dumps(payloadDataCreateVM)
    sendHttpRequest(urlCreateVM, json_data, headers)

createResourceGroup()
createVirtualNetwork()
createSubnet()
createPublicIpAdress()
createNetworkInterface()
createVm()

