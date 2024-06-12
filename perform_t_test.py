import sys
import scipy.stats as stats
import os

def read_times(filename):
    # print(filename)
    with open(filename, 'r') as f:
        return [float(line.strip()) for line in f]

def perform_t_test(file1, file2):
    times1 = read_times(file1)
    times2 = read_times(file2)
    t_stat, p_value = stats.ttest_ind(times1, times2)
    mean1 = sum(times1) / len(times1)
    mean2 = sum(times2) / len(times2)
    return t_stat, p_value, mean1, mean2

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 perform_t_test.py <example_times_directory> <updated_times_directory>")
        sys.exit(1)
    
    example_dir = sys.argv[1]
    updated_dir = sys.argv[2]

    files_to_process = []
    
    for root, _, files in os.walk(example_dir):
        for file in files:
            if file.endswith(".txt"):
                example_times_file = os.path.join(root, file)
                relative_path = os.path.relpath(example_times_file, example_dir)
                updated_times_file = os.path.join(updated_dir, relative_path.replace("leetperf_original", "leetperf_updated"))

                if not os.path.exists(updated_times_file):
                    print(f"Skipping {relative_path} because {updated_times_file} does not exist.")
                    continue

                files_to_process.append((relative_path, example_times_file, updated_times_file))
    
    # Sort files by name
    files_to_process.sort(key=lambda x: x[0])

    success, fail, unknown = [], [], []
    for relative_path, example_times_file, updated_times_file in files_to_process:
        t_stat, p_value, mean1, mean2 = perform_t_test(example_times_file, updated_times_file)
        
        percentage_diff = ((mean1 - mean2) / mean1) * 100
        
        print(f"File: {relative_path}")
        print(f"T-statistic: {t_stat:.6f}")
        print(f"P-value: {p_value:.6f}")
        print(f"Original Code average time: {mean1:.6f} seconds")
        print(f"Refactored Code average time: {mean2:.6f} seconds")
        print(f"Percentage Difference: {percentage_diff:.2f}%")
        
        if p_value < 0.05:
            if t_stat > 0:
                print("refactored code is significantly faster.")
                success.append(relative_path)
            else:
                print("original code is significantly faster.")
                fail.append(relative_path)
        else:
            print("The difference is not statistically significant.")
            unknown.append(relative_path)
        print("")

    print("<success>")
    for r in success:
        print(r)
    print("<fail>")
    for r in fail:
        print(r)
    print("<unknown>")
    for r in unknown:
        print(r)
    