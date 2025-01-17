import csv
import time
import sys
import matplotlib.pyplot as plt

# Increase the maximum recursion depth for large datasets
sys.setrecursionlimit(3000)

# Quick Sort algorithm
def quick_sort(data):
    if len(data) <= 1:
        return data
    
    pivot = data[len(data) // 2]
    less_than_pivot = [item for item in data if int(item[3]) > int(pivot[3])]
    equal_to_pivot = [item for item in data if int(item[3]) == int(pivot[3])]
    greater_than_pivot = [item for item in data if int(item[3]) < int(pivot[3])]

    return quick_sort(less_than_pivot) + equal_to_pivot + quick_sort(greater_than_pivot)

# Merge Sort algorithm
def merge_sort(data):
    if len(data) <= 1:
        return data
    
    mid = len(data) // 2
    left_half = merge_sort(data[:mid])
    right_half = merge_sort(data[mid:])
    
    return merge(left_half, right_half)

def merge(left, right):
    sorted_list = []
    while left and right:
        if int(left[0][3]) > int(right[0][3]):
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))
    sorted_list.extend(left or right)
    return sorted_list

# Read CSV file and return data
def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header line
        data = [row for row in reader]
    return data

# Measure and collect sorting times for Quick Sort and Merge Sort
def process_files(file_paths, sort_function, sort_name):
    times = []
    for i, file_path in enumerate(file_paths, 1):
        print(f"{sort_name} - Processing file {i}: {file_path}")
        start_time = time.time()
        
        # Read and sort CSV data
        data = read_csv(file_path)
        sorted_data = sort_function(data)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        
        print(f"Sorting time for file {i}: {elapsed_time:.4f} seconds")
        print(f"Sample sorted data (first 5 rows): {sorted_data[:5]}")
        print("-" * 40)
    return times

# File paths
file_paths = ["medical_tests.csv", "medical_tests1.csv", "medical_tests2.csv", "medical_tests3.csv"]

# Collect runtime data
quick_sort_times = process_files(file_paths, quick_sort, "Quick Sort")
merge_sort_times = process_files(file_paths, merge_sort, "Merge Sort")

# Plotting the results
dataset_sizes = [f"File {i}" for i in range(1, len(file_paths) + 1)]

plt.figure(figsize=(10, 6))
plt.bar([x for x in range(len(file_paths))], quick_sort_times, width=0.4, label="Quick Sort", align='center')
plt.bar([x + 0.4 for x in range(len(file_paths))], merge_sort_times, width=0.4, label="Merge Sort", align='center')

# Chart labels
plt.xlabel("Dataset (CSV Files)")
plt.ylabel("Sorting Time (seconds)")
plt.title("Performance Comparison of Quick Sort and Merge Sort")
plt.xticks([x + 0.2 for x in range(len(file_paths))], dataset_sizes)
plt.legend()
plt.show()
