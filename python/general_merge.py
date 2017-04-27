import math
import random  

def merge_helper(lines, merge_group, check_merge_criteria):
    merged_lines = []

    remaining_lines = lines[:]
    
    seed_idx = 0 #random.choice(range(len(lines)))
    seed_line = lines[seed_idx]
    groups = [[seed_line]]
    to_remove_idxs = [0]
    current_group_idx = 0
    while (len(remaining_lines)>0):
        for i in xrange(1, len(remaining_lines)):
            growing_line = merge_group(groups[current_group_idx])
            line = remaining_lines[i]
            if (check_merge_criteria(growing_line, line)):
                    groups[current_group_idx].append(line)
                    to_remove_idxs.append(i)
        remaining_lines_copy = []
        for i in xrange(len(remaining_lines)):
            if i not in to_remove_idxs:
                remaining_lines_copy.append(remaining_lines[i][:])
        remaining_lines = remaining_lines_copy
        if (len(remaining_lines)>0):
            current_group_idx += 1
            next_seed = remaining_lines[0]
            groups.append([next_seed])
            to_remove_idxs = [0]

    for group in groups:
        merged_line = merge_group(group)
##        print group
##        for line in group:
##            print get_angle(line)
##        print merged_line
##        print get_angle(merged_line)
        merged_lines.append(merged_line)
##    print len(groups)
    return merged_lines

def merge(lines, merge_group, check_merge_criteria):
    max_iter = 10
    count = 0
    num_lines = len(lines)
    merged_lines = lines
    done = False
    while not done:
        count += 1
        merged_lines = merge_helper(merged_lines, merge_group, check_merge_criteria)
        num_merged_lines = len(merged_lines)
        if (num_merged_lines == num_lines) or (count == max_iter):
            done = True
        else:
            num_lines = num_merged_lines

    return merged_lines
      
