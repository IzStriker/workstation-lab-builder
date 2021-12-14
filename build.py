from workstationfortitude import vmmanagement, vmnetwork
import argparse
import yaml
import sys
from workstationfortitude.interfacecreationexception import InterfaceCreationException
from workstationfortitude.nointerfacesrequired import NoInterfacesRequired

from workstationfortitude.vmnotfound import VMNotFound
from workstationfortitude import auth

def main():
    args = get_args()
    topo = get_topology(args["topology"])

    credentials = auth.encode_credentials(args["username"], args["password"])

    for machine in topo["virtual machines"]:
        # Get parent ID
        parent_id = ""
        try:
            parent_id = vmmanagement.get_vm_id(machine["parent"], credentials)
        except VMNotFound as e:
            sys.exit(e)

        # Clone VM
        res = vmmanagement.clone_vm(machine["name"], parent_id, credentials)

        id = res["id"]

        if("Code" in res):
            print(f"Error {res['Code']}: {res['Message']}")
        

        print(f"Virtual Machine, {machine['name']} created. Memory: {res['memory']}, CPUs: {res['cpu']['processors']}") 

        # Add all interfaces as nat
        try:
            num = vmnetwork.add_interfaces(id, len(machine["adapters"]), credentials)
            print(f"{num} interfaces added to {machine['name']}")
        except NoInterfacesRequired as e:
            print(f"{machine['name']}: {e}")
        except InterfaceCreationException as e:
            print(e)
        
        # Set interface to correct type and network
        vmnetwork.configure_interface_type(machine["adapters"], id, credentials)
        print(f"Adapters set on {machine['name']}")
    


def get_topology(path):
    topo = {}
    try:
        with open(path, "r") as topology:
            try: 
                topo = yaml.safe_load(topology)
            except yaml.YAMLError as e:
                print(e)
    except:
        sys.exit(f"\"{path}\" Not Found")
        
    
    if "virtual machines" not in topo:
        sys.exit("The virtual machines array is missing from topology")

    return topo


def get_args():
    parser = argparse.ArgumentParser(description="VMWare workstation lab builder")
    parser.add_argument("-t", "--topology", help="Path to YAML toplogy file", required=True)
    parser.add_argument("-u", "--username", help="username for vmrest api", required=True)
    parser.add_argument("-p", "--password", help="password for vmrest api", required=True)
    return vars(parser.parse_args())

if __name__ == "__main__":
    main()