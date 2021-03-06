 # VMware Workstation Lab Builder
This is a quick and **dirty** script that automates cloning virtual machines and configuring its network adapters in VMware Workstation Pro. ~~It's entirely possible this script only works on my computers. There isn't even a requirements.txt~~
 ## Use
 This kinda goes without saying, but this script is designed for windows and will get halfway and break if you try to run in on Linux. ~~Who would use workstation pro on Linux anyway when you have KVM.~~

The bulk of the code is in another repo as a submodule, so you need to use the following to clone
```
git clone --recurse-submodules https://github.com/IzStriker/workstation-lab-builder.git
```

The script takes a YAML file defining the topology that is to be created. For Example:
```YAML
virtual machines:
 - name: "lnx-router"
   parent: "Debian 10.x 64-bit"
   linked: true
   adapters:
   - type: "lan"
     name: "DMZ (10.1.1.0/24)"
   - type: "lan"
     name: "Protected Servers (10.2.1.0/24)"
   - type: "nat"
   
 - name: "lnx-server"
   parent: "Debian 10.x 64-bit"
   linked: true
   adapters:
   - type: "lan"
     name: "DMZ (10.1.1.0/24)"

 - name: "lnx-client"
   parent: "Debian 10.x 64-bit"
   linked: false
   adapters:
   - type: "lan"
     name: "Clients (10.2.3.0/24)"
```
There is an array called virtual machines, each VM is an object in that array. Each VM has the following:
 - name -- the name of the VM to be created
 - parent -- the name of the `.vmx` file you want to clone from (exact)
 - linked -- boolean, if the clone should be linked or not (recommend as faster)
 - adapters -- an array of interfaces that will be added to the VM in that order
	 - type -- either `lan` for lan segment or `nat` for nat interface
	 - name -- only requred for `lan` interfaces, created the lan segment before running the script

Nothing special, most of the above is are basic just calls to the `vmrest` API. Except for lan segment, where I had to break out some regex to read and edit configuration files. 
Why lan segments and not custom vmnet adapters? I hate vmnet adapters, they cause more issues than their worth. Why is DHCP enabled by default? Why do you need to know what address range I'm going to use it for? I could go on all day.

Before you try and run the script open a terminal with elevated privileges. Do the following:
```bash
# Navigate to the VMware workstation install folder
cd %programfiles(x86)%\VMware\VMware Workstation\ 
# Set the vmrest login details (Only the first time)
vmrest -C # Following the instructions
# Then start the server
vmrest
```
Yes I know, I should be using SSL. I'm not, you can if you want.

Then start the script:
```bash
 python .\build.py -t .\<topology>.yaml -u "<username>" -p "<password>"
```
replacing all the relevant parts. 

Don't have workstation open when you're running this script, it doesn't really make a difference though as the VMs are registered after all configuration is done. Make sure to get the names of the parent VM you're trying to clone from correct. Make sure you provide the correct names for the lan segments. Try not to make any mistakes in the YAML in general, it yield may unexpected results with half build VMs.

I don't think I've missed anything, this readme is really for me when I forget how to use this script. 
