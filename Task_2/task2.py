import pandas as pd  # For reading and handling CSV data
import time
import matplotlib.pyplot as plt
import csv
#Function to create a data list by reading a CSV file
def read_csv_file(file_path):
    data = [] # A structure that makes our job easier for storing and later processing the data read from the CSV file.
    # Read the CSV file
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

"""
def binary_search(array, target):
    left = 0  # Dizinin başlangıç indeksi
    right = len(array) - 1  # Dizinin son indeksi

    while left <= right:  # Sol ve sağ sınırlar çakışmadığı sürece devam et
        mid = (left + right) // 2  # Ortadaki indeksi hesapla
        if array[mid] == target:  # Ortadaki eleman aranan öğeye eşitse
            return mid  # Ortadaki indeksi döndür
        elif array[mid] < target:  # Aranan öğe ortadakinden büyükse
            left = mid + 1  # Sol sınırı sağa kaydır
        else:  # Aranan öğe ortadakinden küçükse
            right = mid - 1  # Sağ sınırı sola kaydır

    return -1  # Aranan öğe bulunamadığında -1 döndür


"""


#Binary Search Algorithm for exact matching
# for ordered list
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        product_name = arr[mid]["Product Name"].strip().lower()
        if product_name == target.lower(): #Is there a match to the target?
            return mid
        elif product_name < target.lower():
            left = mid + 1
        else:
            right = mid - 1
    return -1


"""
def linear_search(array, target):
    for index in range(len(array)):  # Dizinin tüm elemanlarını sırayla dolaş
        if array[index] == target:  # Aranan öğe ile mevcut elemanı karşılaştır
            return index  # Bulduğunda öğenin indeksini döndür
    return -1  # Aranan öğe bulunamadığında -1 döndür

"""


# Linear Search Algorithm for partial matching
# from beggining to the end
def partial_search(arr, keyword):
    results = []
    for i, item in enumerate(arr): 
        if keyword.lower() in item["Product Name"].lower(): #Is there a keyword in the product name?
            results.append((i, item)) #If a match is found, add the index and item to the list
    return results

# Performance measurement function
def measure_performance(data, keyword, dataset_name, csv_writer):
    # Binary Search performance measurement
    start_time = time.perf_counter() #Starting time
    index = binary_search(data, keyword)
    binary_search_time = time.perf_counter() - start_time #Execution time

    # Result of exact matching
    binary_result = 1 if index != -1 else 0 #Is there a match? 1 (positive), 0 (negative)

    # Linear Search performance measurement
    start_time = time.perf_counter() #Starting time
    matches = partial_search(data, keyword) #Finds partial matching
    linear_search_time = time.perf_counter() - start_time #Execution Time

    #Preparing partial matching results
    partial_result_count = len(matches) #Number of partial matching
    partial_result_text = "\n".join([f"({i}, {item})" for i, item in matches])

    #Print dataset results to CSV
    csv_writer.writerow([
        f"---------- {dataset_name} ----------\n",
        f"Exact Match: {binary_result}",
        f"Partial Match: {partial_result_count} \n",
        partial_result_text ])

    return binary_search_time, linear_search_time

# Function to process data sets and collect search times
def process_datasets(file_paths, keyword, output_file):
    binary_times = []
    linear_times = []
    dataset_labels = []
    # Open a CSV file to write results
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)

        for i, file_path in enumerate(file_paths, start=1):
            dataset_name = f"Dataset {i}"
            print(f"\n{'-'*10} {dataset_name} {'-'*10}") #Print dataset name to console

            data = read_csv_file(file_path)
            data.sort(key=lambda x: x["Product Name"].strip())

            # Measure performance
            binary_time, linear_time = measure_performance(data, keyword, dataset_name, csv_writer)

            # Collect times for plotting
            binary_times.append(binary_time)
            linear_times.append(linear_time)
            dataset_labels.append(dataset_name)

            # Print times to console
            print(f"Binary Search Time: {binary_time:.8f} seconds")
            print(f"Linear Search Time: {linear_time:.8f} seconds")

    # Plot the search times using matplotlib
    plt.figure(figsize=(10, 6))
    x = range(len(file_paths))
    plt.bar([i - 0.2 for i in x], binary_times, width=0.4, label='Binary Search')
    plt.bar([i + 0.2 for i in x], linear_times, width=0.4, label='Linear Search')

    plt.xlabel("Datasets")
    plt.ylabel("Time (seconds)")
    plt.title("Comparison of Binary and Linear Search Efficiency")
    plt.xticks(x, dataset_labels)
    plt.legend()
    plt.tight_layout()
    plt.show()

# List of file paths and keyword input
file_paths = ['product_catalog.csv', 'product_catalog1.csv', 'product_catalog2.csv', 'product_catalog3.csv']
output_file = 'search_results.csv'
keyword = input("Which product do you want to search for?: ")

# Process datasets and plot efficiency
process_datasets(file_paths, keyword, output_file)
