with open('data/Challenge_FedEx.txt', 'r') as file:
    lines = file.readlines()
uld_count = int(lines[0]) 
ulds = {}
line_index = 1
uld_volumes = []
for _ in range(uld_count):
    uld_data = lines[line_index].split(",")
    uld_id=uld_data[0]
    length=uld_data[1]
    width=uld_data[2]
    height=uld_data[3]
    capacity=uld_data[4]
    # ulds[uld_id] = ULD(uld_id, int(length), int(width), int(height), int(capacity))
    uld_volumes.append(int(length)*int(width)*int(height))
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
priority_volumes = []
economic_volumes = []
for _ in range(package_count):
    package_data = lines[line_index].split(",")
    package_id, length, width, height, weight, priority, delay = package_data
    priority = priority.strip()
    if priority != "Priority":
        volumes.append(int(length)*int(width)*int(height))
        delays.append(int(delay))
        total_delay += int(delay)
        economic_volumes.append(int(length)*int(width)*int(height)) 
    else:
        priority_volumes.append(int(length)*int(width)*int(height))
        
    weight = int(weight)
    delay = delay
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
            # print(i, j)
# print(i, len_of_unique)

# print(non_unique)
# print(200*399)
    
# print(total_delay)

# K = int(lines[line_index]) 

# # return ulds, packages, K

# import scipy.stats as stats 

# #get correlation matrix
# correlation_matrix = stats.spearmanr(volumes, delays)
# print(correlation_matrix)

# print(sum(uld_volumes))
# print("Average delay", total_delay/len(economic_volumes))
# print("Average Economic Volume", sum(economic_volumes)/len(economic_volumes))
# print("Priority", sum(priority_volumes))
# print("Economic", sum(economic_volumes))
# print("Total", sum(priority_volumes) + sum(economic_volumes))
# print("Total - Priority", sum(uld_volumes) - sum(priority_volumes))
# print("Rough Economic Boxes Remaining", (sum(uld_volumes) - sum(priority_volumes))*len(economic_volumes)/sum(economic_volumes))
# print("Left out economic boxes", len(economic_volumes)- (sum(uld_volumes) - sum(priority_volumes))*len(economic_volumes)/sum(economic_volumes))
# print("Percentage", (sum(priority_volumes) + sum(economic_volumes))/sum(uld_volumes)*100)
# print("Economic Percentage", sum(economic_volumes)/sum(uld_volumes)*100)
# print("Priority Percentage", sum(priority_volumes)/sum(uld_volumes)*100)
# print("Economy after priority", sum(economic_volumes)/(sum(uld_volumes) - sum(priority_volumes))*100)

print("Sum of all ULD Volumes:", sum(uld_volumes))
print("Average Delay of Economic Boxes:", total_delay/len(economic_volumes))
print("Average Economic Volume:", sum(economic_volumes)/len(economic_volumes))
print("Sum of Priority Volumes:", sum(priority_volumes))
print("Sum of Economic Volumes:", sum(economic_volumes))
print("Total Package Volume:", sum(priority_volumes) + sum(economic_volumes))
print("Total ULD Volume - Priority:", sum(uld_volumes) - sum(priority_volumes))
print("Rough Estimate of Economic Boxes that can be fitted:", (sum(uld_volumes) - sum(priority_volumes))*len(economic_volumes)/sum(economic_volumes))
print("Rough Estimate of Economic Boxes left out:", len(economic_volumes)- (sum(uld_volumes) - sum(priority_volumes))*len(economic_volumes)/sum(economic_volumes))
print("Rough Estimate of Economic Cost with the rough estimate:", total_delay- (sum(uld_volumes) - sum(priority_volumes))*total_delay/sum(economic_volumes))

# import 