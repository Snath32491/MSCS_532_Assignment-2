import random
import time
import tracemalloc
import sys
import matplotlib.pyplot as plt
import pandas as pd

sys.setrecursionlimit(10000)

# ---------------- SORTING ALGORITHMS ----------------

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort(left)
        merge_sort(right)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

# ---------------- TESTING & MEASUREMENT ----------------

results = []

def run_and_measure(sort_func, arr, algo_name, dataset_name):
    arr_copy = arr.copy()
    tracemalloc.start()
    start_time = time.perf_counter()

    if algo_name == "Quick Sort":
        sort_func(arr_copy, 0, len(arr_copy) - 1)
    else:
        sort_func(arr_copy)

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    exec_time = round((end_time - start_time) * 1000, 3)  # in ms
    peak_mem = round(peak / 1024, 3)  # in KB

    print(f"{algo_name} on {dataset_name} data:")
    print(f"  Time taken      : {exec_time} ms")
    print(f"  Peak memory     : {peak_mem} KB")
    print("-" * 50)

    results.append({
        "Algorithm": algo_name,
        "Dataset": dataset_name,
        "Time (ms)": exec_time,
        "Memory (KB)": peak_mem
    })

# ---------------- MAIN ----------------

def main():
    size = 1000  # Feel free to increase for larger testing
    sorted_data = list(range(size))
    reverse_data = list(range(size, 0, -1))
    random_data = [random.randint(1, 10000) for _ in range(size)]

    datasets = [
        ("Sorted", sorted_data),
        ("Reverse Sorted", reverse_data),
        ("Random", random_data)
    ]

    for name, data in datasets:
        run_and_measure(merge_sort, data, "Merge Sort", name)
        run_and_measure(quick_sort, data, "Quick Sort", name)

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Save to CSV
    df.to_csv("sorting_results.csv", index=False)
    print("\n Results saved to 'sorting_results.csv'")

    # Plot graphs
    plot_results(df)

# ---------------- PLOTTING ----------------

def plot_results(df):
    plt.figure(figsize=(10, 6))
    for metric in ["Time (ms)", "Memory (KB)"]:
        plt.clf()
        pivot = df.pivot(index="Dataset", columns="Algorithm", values=metric)
        pivot.plot(kind='bar', figsize=(10, 6))
        plt.title(f"{metric} Comparison")
        plt.ylabel(metric)
        plt.xlabel("Dataset Type")
        plt.xticks(rotation=0)
        plt.tight_layout()
        filename = f"{metric.replace(' ', '_').replace('(', '').replace(')', '')}_comparison.png"
        plt.savefig(filename)
        print(f" {metric} graph saved as '{filename}'")

# ---------------- RUN ----------------

if __name__ == "__main__":
    main()
