with open('data/Challenge_FedEx.txt', 'r') as file:
    lines = file.readlines()
uld_count = int(lines[0]) 
ulds = {}
line_index = 1
for _ in range(uld_count):
    uld_data = lines[line_index].split(",")
    uld_id=uld_data[0]
    length=uld_data[1]
    width=uld_data[2]
    height=uld_data[3]
    capacity=uld_data[4]
    # ulds[uld_id] = ULD(uld_id, int(length), int(width), int(height), int(capacity))
    line_index += 1

package_count = int(lines[line_index]) 
packages = {}
line_index += 1

# package_dim = set()
i=0
package_dim_list = []
package_weight_list = []
total_delay = 0
volumes = []
delays = []
for _ in range(package_count):
    package_data = lines[line_index].split(",")
    package_id, length, width, height, weight, priority, delay = package_data
    priority = priority.strip()
    if priority != "Priority":
        volumes.append(int(length)*int(width)*int(height))
        delays.append(int(delay))
    weight = int(weight)
    delay = delay
    total_delay += int(delay)
    # packages[package_id] = Package(package_id, int(length), int(width), int(height), weight, priority, delay)
    line_index += 1
    package_dim_list.append(([int(length), int(width), int(height)]))
    package_weight_list.append(weight)
    i += 1
    
# print(package_dim_list)
# print(package_weight_list)
# len_of_unique = len(set(package_dim_list))
non_unique = 0
for i in range(0, len(package_dim_list)):
    package_i_list = sorted(list(package_dim_list[i]))
    for j in range(i+1, len(package_dim_list)):
        package_j_list = sorted(package_dim_list[j])
        # print(package_j_list)
        # if package_i_list[0] == package_j_list[0] or package_i_list[1] == package_j_list[1] or package_i_list[2] == package_j_list[2]:
        if package_i_list[0] in package_j_list or package_i_list[1] in package_j_list or package_i_list[2] in package_j_list:
            non_unique += 1
            print(i, j)
# print(i, len_of_unique)

# print(non_unique)
# print(200*399)
    
print(total_delay)

K = int(lines[line_index]) 

# return ulds, packages, K

import scipy.stats as stats 

#get correlation matrix
correlation_matrix = stats.spearmanr(volumes, delays)
print(correlation_matrix)

import 