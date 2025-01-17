import pandas as pd
import time
import bisect
import matplotlib.pyplot as plt

# Load multiple CSV files and return sorted document IDs and documents
def load_documents_from_csv(file_paths):
    """Loads and concatenates multiple CSV files, sorts them by Document ID,
    and returns a list of sorted document IDs and documents as dictionaries."""
    try:
        # Concatenate files
        all_data = pd.concat((pd.read_csv(f) for f in file_paths), ignore_index=True)

        # Sort documents by Document ID
        all_data = all_data.sort_values('Document ID').reset_index(drop=True)

        # Get document IDs as a sorted list
        document_ids = all_data['Document ID'].tolist()

        # Convert documents to a list
        documents = all_data.to_dict(orient='records')

        return document_ids, documents
    except Exception as e:
        print(f"Error reading CSV files: {e}")
        return [], []

# Exact Document ID Search Function (Binary Search)
def find_document_by_id(document_id, document_ids, documents):
    """Performs Binary Search to find a document by exact ID."""
    start_time = time.time()  # Record start time
    index = bisect.bisect_left(document_ids, document_id)
    if index < len(document_ids) and document_ids[index] == document_id:
        document = documents[index]
        end_time = time.time()  # Record end time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        return document, elapsed_time  # Return document and time
    else:
        return None, None  # If document not found

# Partial Match Search Function (Exact Keyword Match)
def find_document_by_partial_metadata(keyword, documents):
    """Searches for documents by exact match in 'Document Title' or 'Author'."""
    start_time = time.time()  # Record start time
    results = [doc for doc in documents if
               doc['Document Title'] == keyword or doc['Author'] == keyword]
    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    return results, elapsed_time  # Return matching documents and time

# Test Binary Search performance
def test_binary_search(document_ids, documents, search_id, repetitions=10000):
    """Tests Binary Search and returns the average elapsed time over a number of repetitions."""
    start_time = time.perf_counter()
    for _ in range(repetitions):
        find_document_by_id(search_id, document_ids, documents)
    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) / repetitions  # Average time per search
    return elapsed_time

# Test Linear Search performance
def test_linear_search(documents, keyword, repetitions=100):
    """Tests Linear Search and returns the average elapsed time over a number of repetitions."""
    start_time = time.perf_counter()
    for _ in range(repetitions):
        find_document_by_partial_metadata(keyword, documents)
    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) / repetitions  # Average time per search
    return elapsed_time

# Run tests on each dataset
def run_tests_for_datasets(csv_file_paths, search_id, keyword):
    """Loads the dataset and runs performance tests for both search methods."""
    document_ids, documents = load_documents_from_csv(csv_file_paths)

    # Test Binary Search with a high number of repetitions
    binary_time = test_binary_search(document_ids, documents, search_id)

    # Test Linear Search
    linear_time = test_linear_search(documents, keyword)

    # Return both search times
    return binary_time, linear_time

# Plot the performance results
def plot_performance(dataset_sizes, binary_times, linear_times):
    """Plots the search performance of Binary Search vs Linear Search."""
    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, binary_times, label="Binary Search Time (s)", marker='o')
    plt.plot(dataset_sizes, linear_times, label="Linear Search Time (s)", marker='o')
    plt.xlabel("Dataset Size")
    plt.ylabel("Search Time (s)")
    plt.title("Binary Search vs Linear Search Performance")
    plt.legend()
    plt.grid(True)
    plt.xscale("log")  # Use logarithmic scale for better visualization
    plt.yscale("log")  # Log scale on y-axis as well to highlight time differences
    plt.show()

# Main program with both terminal search and performance testing
if __name__ == "__main__":
    # Example search values (adjust as needed for your test cases)
    search_id = 10  # Choose an ID that exists in all files for consistency
    keyword = "Author 10"  # Adjust the keyword to test partial metadata search

    # Define different dataset sizes with the respective file paths
    data_sizes = {
        "10": ['document_archive.csv'],
        "100": ['document_archive1.csv'],
        "1K": ['document_archive2.csv'],
        "10K": ['document_archive3.csv']
    }

    # Initialize lists for storing results
    dataset_sizes = []
    binary_times = []
    linear_times = []

    # Run tests for each dataset size and collect results
    print(f"{'Dataset Size':<10} {'Binary Search Time (s)':<25} {'Linear Search Time (s)':<25}")
    print("=" * 60)

    for size, paths in data_sizes.items():
        binary_time, linear_time = run_tests_for_datasets(paths, search_id, keyword)
        dataset_sizes.append(int(size.replace("K", "000") if "K" in size else size))
        binary_times.append(binary_time)
        linear_times.append(linear_time)
        print(f"{size:<10} {binary_time:<25.8f} {linear_time:<25.8f}")

    # Plot performance results
    plot_performance(dataset_sizes, binary_times, linear_times)

    # Load documents for real-time search
    document_ids, documents = load_documents_from_csv([file for path in data_sizes.values() for file in path])

    # Interactive terminal-based search
    while True:
        print("\n1. Search by Exact Document ID")
        print("2. Search by Partial Title/Author")
        print("Enter -1 to exit")
        choice = input("Your choice: ")

        if choice == '-1':
            break
        elif choice == '1':
            user_input = input("Enter the Document ID you want to search for: ")
            try:
                search_id = int(user_input)
                document, search_time = find_document_by_id(search_id, document_ids, documents)
                if document is not None:
                    print(f"Document found: {document}\nSearch Time: {search_time:.6f} seconds")
                else:
                    print(f"Document ID {search_id} not found.")
            except ValueError:
                print("Invalid input! Please enter a valid Document ID.")
        elif choice == '2':
            keyword = input("Enter the title or author keyword you want to search for: ")
            results, search_time = find_document_by_partial_metadata(keyword, documents)
            if results:
                print(f"{len(results)} document(s) found:\n{results}\nSearch Time: {search_time:.6f} seconds")
            else:
                print(f"No document found with the keyword '{keyword}'.")
        else:
            print("Invalid selection! Please enter 1, 2, or -1.")
