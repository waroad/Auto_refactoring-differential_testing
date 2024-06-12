import time
import random
import subprocess

# Function to generate random inputs and run the sorting script
#  2750, 17608 용
def test_sorting_script(num_tests=10, max_n=200000, max_value=1000000):
    total_time1 = 0
    total_time2 = 0
    for _ in range(num_tests):
        n = random.randint(100000, max_n)
        inputs = [str(n)] + [str(random.randint(1, max_value)) for _ in range(n)]

        # Prepare the input as a single string
        input_str = "\n".join(inputs) + "\n"

        start_time = time.time()

        # Run the sort_script.py and pass the input_str to it
        process = subprocess.Popen(['python3', 'temp1.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate(input=input_str.encode())

        end_time = time.time()
        total_time1 += (end_time - start_time)

        start_time = time.time()

        # Run the sort_script.py and pass the input_str to it
        process = subprocess.Popen(['python3', 'temp2.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate(input=input_str.encode())

        end_time = time.time()
        total_time2 += (end_time - start_time)

    print(f"Total time spent on {num_tests} runs for original: {total_time1:.2f} seconds")
    print(f"Average time per run: {total_time1/num_tests:.4f} seconds")
    print(f"Total time spent on {num_tests} runs for refactored: {total_time2:.2f} seconds")
    print(f"Average time per run: {total_time2/num_tests:.4f} seconds")
    print(f"{total_time1/total_time2: .4f} times faster")

if __name__ == "__main__":
    test_sorting_script()
