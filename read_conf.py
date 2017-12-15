import csv
import re
import os


def network_address_str(ip, mask):
    ip_dec_str = ip.split(".")
    mask_dec_str = mask.split(".")
    netw_add_int = []
    mask_len = 0
    mask_part_dict = {"255": 8, "254": 7, "252": 6, "248": 5, "240": 4, "224": 3, "192": 2, "128": 1, "0": 0}
    for i in range(0, 4):
        netw_add_int.append(str(int(ip_dec_str[i]) & int(mask_dec_str[i])))
        mask_len += mask_part_dict[mask_dec_str[i]]
    result = '.'.join(netw_add_int)+"/"+str(mask_len)
    return result


# print(network_address("192.168.1.143","255.255.255.252"))
# input()
def make_vlan_list(conf_name):
    with open(conf_name, "r") as file:
        a = file.readlines()
    vlan_list = []
    buff = ()
    for i in range(len(a)):
        if a[i].startswith("interface Vlan"):
            buff += ((re.search(r" (Vlan\d+)\n", a[i])).group(1),)
            # print (buff)

            #while a[i].startswith(" "):
            if a[i+1].startswith(" description "):
                buff += ((re.search(r"n (.+)\n", a[i+1])).group(1),)
                i += 1
            else:
                buff += (" ",)
                # i += 1
            # print(buff)
            if a[i+1].startswith(" ip ad"):
                regex_ip_mask = re.search(r"s ((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}"
                                          r"([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])) "
                                          r"((255\.|254\.|252\.|248\.|240\.|224\.|192\.|128\.|0\.){3}"
                                          r"(255|252|248|240|224|192|128|0))", a[i+1])
                buff += (regex_ip_mask.group(1),)
                buff += (network_address_str(regex_ip_mask.group(1), regex_ip_mask.group(5)),)
                # break
                # print(regex_ip_mask.group(),)
                i += 1
            else:
                buff += (" ", " ",)
            vlan_list.append(buff)
            buff = ()
            # input()
            # print("List: ", vlan_list)
    return vlan_list


Dir_path = input("Dir path: ", )
List_of_configs = os.listdir(Dir_path)
Output_dir = Dir_path+"/vlans_csv/"
for config in List_of_configs:
    if os.path.isfile(Dir_path+"/"+config):
        vlan_list_of_current_config = make_vlan_list(Dir_path+"/"+config)
        with open(Output_dir+config+".csv", "w", newline="") as out:
            csv_out = csv.writer(out)
            csv_out.writerow(["Vlan number", "Description", "Vlan int ip", "Network"])
            for row in vlan_list_of_current_config:
                # print(row)
                # input()
                csv_out.writerow(row)
    # input()