import pandas as pd  # For reading and handling CSV data
import time
import matplotlib.pyplot as plt  # For plotting results

# Bubble Sort Algorithm Implementation
def bubble_sort(array):
    length = len(array)
    for i in range(length):
        for j in range(0, length - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array

# Merge Sort Algorithm Implementation
def merge_sort(array):
    if len(array) <= 1:
        return array
    midpoint = len(array) // 2
    left_half = merge_sort(array[:midpoint])
    right_half = merge_sort(array[midpoint:])
    return merge(left_half, right_half)

# Helper function for Merge Sort to merge two sorted halves
def merge(left_half, right_half):
    sorted_result = []
    i = j = 0
    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:
            sorted_result.append(left_half[i])
            i += 1
        else:
            sorted_result.append(right_half[j])
            j += 1
    sorted_result.extend(left_half[i:])
    sorted_result.extend(right_half[j:])
    return sorted_result

# Function to measure the time taken by a sorting algorithm
def measure_sorting_time(sorting_function, array, algorithm_name):
    start_time = time.time()
    sorted_array = sorting_function(array.copy())
    end_time = time.time()
    return end_time - start_time

# Dictionary to map dataset sizes to file names
datasets = {
    'small': 'customer_orders.csv',
    'medium': 'customer_orders1.csv',
    'large': 'customer_orders2.csv',
    'xlarge': 'customer_orders3.csv'
}

# Lists to store sorting times for Bubble Sort and Merge Sort
bubble_sort_times = []
merge_sort_times = []

# Loop through each dataset, reading the data and timing the sorts
for size_label, filename in datasets.items():
    # Read the CSV file into a DataFrame
    data = pd.read_csv(filename)

    # Display the first 5 rows of the current file
    print(f"\nFirst 5 rows of {filename} ({size_label} dataset):")
    print(data.head())

    # Extract 'Order Amount' column as a list of numbers
    order_amounts = data['Order Amount'].tolist()

    print(f"\n{size_label.capitalize()} dataset result:")
    # Measure and record Bubble Sort time
    bubble_time = measure_sorting_time(bubble_sort, order_amounts, "Bubble Sort")
    # Measure and record Merge Sort time
    merge_time = measure_sorting_time(merge_sort, order_amounts, "Merge Sort")

    # Append times to respective lists for plotting later
    bubble_sort_times.append(bubble_time)
    merge_sort_times.append(merge_time)

    # Print the time taken for each sort
    print(f"Bubble Sort time: {bubble_time:.6f} seconds")
    print(f"Merge Sort time: {merge_time:.6f} seconds")

# Plotting the sorting times for each dataset size
plt.figure(figsize=(10, 6))
plt.bar(datasets.keys(), bubble_sort_times, width=0.4, label='Bubble Sort', color='blue', align='center')
plt.bar(datasets.keys(), merge_sort_times, width=0.4, label='Merge Sort', color='orange', align='edge')

# Set y-axis limit for better visualization
plt.ylim(0, 0.05)

# Labeling the plot
plt.xlabel('Dataset Size')
plt.ylabel('Sorting Time (seconds)')
plt.title('Performance Comparison of Sorting Algorithms')
plt.legend()
plt.show()

