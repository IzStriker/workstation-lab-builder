import argparse
import yaml

def main():
    args = get_args()
    get_topology(args["topology"])

def get_topology(path):
    topo = {}
    try:
        with open(path, "r") as topology:
            try: 
                topo = yaml.safe_load(topology)
            except yaml.YAMLError as e:
                print(e)
    except:
        print(f"\"{path}\" Not Found")
    
    if "virtual machines" not in topo:
        print("The virtual machines array is missing from topology")


def get_args():
    parser = argparse.ArgumentParser(description="VMWare workstation lab builder")
    parser.add_argument("-t", "--topology", help="Path to YAML toplogy file", required=True)
    return vars(parser.parse_args())

if __name__ == "__main__":
    main()