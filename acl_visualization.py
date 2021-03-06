import re
# import os


def list_from_file(path):
    try:
        with open (path,'r') as f:
            output = f.readlines()
            for row in output:
                output[output.index(row)] = row.strip("\n")
        return output
    except (OSError, IOError) as e:
        print ("Check Filepath")


def make_acl_dict(config):
    acl_dict = {}
    acl = []
    ex_acl_f = False
    same_std_acl = False
    # for string in config:                               # for cycle without pointer
    #     if string.startswith("ip access-list extended "):
    #         name = re.search(r'^ip access-list extended (\w+)',string).group(1)
    #         ex_acl_f = True
    #         continue
    #     if string.startswith(" ") and ex_acl_f:
    #         acl.append(string)
    #
    #
    #    if string.startswith("access-list "):            # for cycle without pointer
    for i in range(len(config)):
        if config[i].startswith("ip access-list extended "):
            name = re.search(r'^ip access-list extended (\w+)',config[i].strip("\n")).group(1)
            ex_acl_f = True
            continue
        elif config[i].startswith(" ") and ex_acl_f:
            acl.append(config[i].strip("\n"))
            if not config[i+1].startswith(" "):
                ex_acl_f = False
                acl_dict[name] = acl
                acl = []
            continue
        elif config[i].startswith("access-list ") and not same_std_acl:
            match = re.search(r'^access-list (\d+) (.+)$',config[i].strip("\n"))
            name = match.group(1)
            same_std_acl = True
            acl.append(match.group(2))
            continue
        elif config[i].startswith("access-list ") and same_std_acl:
            acl.append(re.search(r'^access-list (\d+) (.+)$',config[i].strip("\n")).group(2))
            if not config[i+1].startswith("access-list "+name):
                same_std_acl = False
                acl_dict[name] = acl
                acl = []
                # print (acl_dict[name])
                # input()
            continue
        else:
            continue
    return acl_dict


def make_int_dict(config):                                  # Config as list
    int_dict = {}
    int_attr = []
    int_f = False
    name = "no interfaces in this config"
    for i in range(len(config)):
        if config[i].startswith("interface "):
            name = re.search(r'interface ((\w+.+)|(\w+))',config[i].strip("\n")).group(1)
            int_f = True
            continue
        elif config[i].startswith(" ") and int_f:
            # print(config[i])
            # input()
            int_attr.append(config[i].strip("\n"))
            if not config[i+1].startswith(" "):
                int_f = False
                int_dict[name] = int_attr
                int_attr = []
            continue
        else:
            continue
    return int_dict


def network_address(input_string):
    net_addr_1 = "0.0.0.0"
    if input_string.startswith(" ip address"):
        ip_addr_mask = re.search(r' ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)',input_string)
        ip_addr = ip_addr_mask.group(1).split('.')
        mask = ip_addr_mask.group(2).split('.')
        temp = []
        for oct in range(4):
            temp.append(str(int(ip_addr[oct]) & int(mask[oct])))   #network ip address as a list
        net_addr_1 = ".".join(temp)+" "+ip_addr_mask.group(2)
    return net_addr_1


def l3_interfaces(int_dict):
    # Input type dictionary of interfaces
    _l3_int_dict = {}
    for int in int_dict:
        for attr in int_dict[int]:
            if attr.startswith(" ip address"):
                _l3_int_dict[int] = int_dict[int]
                break
    return _l3_int_dict

def no_shut_l3_to_file(_l3_int_dict, filepath):
    # f_5int = False
    index = 1
    with open(filepath, "w", newline="") as out:
        out.write("interface range ")
        for int in _l3_int_dict:
            if " shutdown" in _l3_int_dict[int]:
                continue
            elif index % 5 != 0:
                index += 1
                out.write(int+" , ")
            else:
                index += 1
                out.write(int+"\n")
                out.write("interface range ")

# def find_matching_network(list):


# def make_SW_HostGroup_dict(vlan_list):
#     ##############################################
#     # Input list made from vlan/ip_addr cvs file #
#     ##############################################
#     group_dict = {}
#     for row in vlan_list:
#         group_dict[]


def make_List_of_Vlan_Dict(list):
    #################################################
    # Input is csv file containing columns named: 'subnet', 'mask', 'vlan_id',
    #                                             'vlan_description', 'gateway', 'location'
    # Output is a list of dictionaries containing early mentioned vlan info
    #################################################
    List_of_Vlan_Dict = []
    clmn_names = list[0].split(";")                 # key names for dictionaries
    for row in list[1:]:
        tmp_dict = {}
        clmns = row.split(";")
        for i in range(len(clmns)):
            tmp_dict[clmn_names[i]] = clmns[i]
        List_of_Vlan_Dict.append(tmp_dict)          # List filling
    return List_of_Vlan_Dict

def all_locations(list_of_dict):
    #################################################
    # Input is ONLY a list of dictionaries containing early mentioned vlan info
    # Output is a set of locations
    #################################################
    loc_set = set()
    for _vlan_ in list_of_dict:
        loc_set.add(_vlan_["location"])
    return loc_set




#while True:
workdir = "C:/PY/FA/configs/"                       # Default dir with config
conf_filename = "6503_RAS"                          # Certain config filename
#
# Insert function making an abspath to config file
#
conf_abspath = workdir+conf_filename
vlan_ip_abspath = "C:/PY/FA/vlans/fosagro_vlan_ip_1.csv"
l1 = list_from_file(conf_abspath)                   #
l2 = list_from_file(vlan_ip_abspath)                # network ip, vlan, description etc
# for row in l2:
#     l2[l2.index(row)] = row.strip("\n")
all_acl = make_acl_dict(l1)
all_int = make_int_dict(l1)
# print (all_acl)
# input ()
for key in all_int:                                 # Network Address at the end of int param list
    # # print (key)
    # descr_f = False
    # # param_list = all_int[key]
    for string in all_int[key]:
        # if not string.startswith(" description"):
        #     # all_int[key].insert(0, "")
        #     descr_f = True
        #     # continue
        if string.startswith(" ip address"):
            net_addr = network_address(string)
            all_int[key].append(net_addr)
            if not all_int[key][0].startswith(" description"):
                all_int[key].insert(0, "")          # Make sure ip address is at [1] position
            # print (all_int[key])
            break
IF_csv_d = {}
# for key in all_int:
#     IF_csv_d[key] = []
#     IF_csv_d[key].append(all_int[key][0])           # Add description row
#     IF_csv_d[key].append(all_int[key][1])           # Add IP address row
#     for row in l2:
#         CLMN = row.split(";")                       # Make columns from l2.row
#         # IF_csv_d[key].append(all_int[key][1])          # Add IP address row
#         #
#         # Adding information from l2.row if Network IP address matched
#         #
#         if all_int[key][len(all_int[key])-1] == (CLMN[0]+" "+CLMN[1]).strip(" "):
#             # print (CLMN)
#             IF_csv_d[key].append("Vlan "+CLMN[3].strip(" ")+" - "+CLMN[2].strip(" "))
#             int_ip = re.search(r'^ ip address (\d+\.\d+\.\d+\.\d+) .+',IF_csv_d[key][1]).group(1)
#             GW = CLMN[4].strip(" ")
#             if int_ip == GW:
#                 IF_csv_d[key].append("This interface is GW")
#             else:
#                 IF_csv_d[key].append("GW is "+GW)
#             IF_csv_d[key].append(CLMN[5].strip(" "))
# #    for key in IF_csv_d:
# #    break