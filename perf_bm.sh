#!/bin/bash

# Number of iterations
ITERATIONS=50

# Function to measure time
measure_time() {
    local file=$1
    local output_file=$2
    echo -n "" > $output_file  # Clear the output file

    for ((j=0; j<$ITERATIONS; j++)); do
        elapsed=$(python3 $file | grep "Elapsed time" | awk '{print $3}')
        echo $elapsed >> $output_file
    done
}

example_files=(examples/success/*.py)
updated_files=(updated/success/*.py)
if [[ ${#example_files[@]} -ne ${#updated_files[@]} ]]; then
    echo "The number of .py files in example_test/simple and updated_test/simple do not match."
    exit 1
fi

# File indices
for ((i=0; i<${#example_files[@]}; i++)); do
    example_file=${example_files[i]}
    updated_file=${updated_files[i]}
    
    # Extract base file name without directory and extension
    base_name=$(basename $example_file .py)
    
    example_output="leetperf_original/${base_name}.txt"
    updated_output="leetperf_updated/${base_name}.txt"
    
    echo "$updated_file start"
    measure_time $updated_file $updated_output
    
    echo "$example_file start"
    measure_time $example_file $example_output

    # Call Python script to perform t-test
    python3 perform_t_test.py $example_output $updated_output "${base_name}.py"
done
