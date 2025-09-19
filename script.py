import random
import subprocess
import os
import csv

def binary_to_gray(bin_str):
    val = int(bin_str, 2)
    gray_val = val ^ (val >> 1)
    return format(gray_val, '04b')

def gray_to_binary(gray_str):
    val = int(gray_str, 2)
    mask = val >> 1
    while mask != 0:
        val = val ^ mask
        mask = mask >> 1
    return format(val, '04b')

def run_verilog_tb(tb_file, module_file, input_list, input_type):
    input_filename = "input_binary.txt" if input_type == 'binary' else "input_gray.txt"
    with open(input_filename, "w") as f:
        for vec in input_list:
            f.write(f"{vec}\n")

    tb_name = "tb_binary_to_gray.v" if input_type == 'binary' else "tb_gray_to_binary.v"
    module_name = "binary_to_gray.v" if input_type == 'binary' else "gray_to_binary.v"
    compile_cmd = ["iverilog", "-o", "tb_run", module_name, tb_name]
    run_cmd = ["vvp", "tb_run"]
    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
        sim_output = subprocess.run(run_cmd, check=True, capture_output=True, text=True)
        output_lines = sim_output.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error running {tb_name}: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return []
    except FileNotFoundError:
        print("Error: 'iverilog' or 'vvp' not found.")
        return []
    finally:
        if os.path.exists("tb_run"):
            os.remove("tb_run")
        if os.path.exists(input_filename):
            os.remove(input_filename)

    results = []
    for line in output_lines:
        if "Input" in line and "Output" in line:
            parts = line.replace(",", "").split()
            if input_type == 'binary':
                bin_in = parts[2]
                gray_out = parts[-1]
                results.append((bin_in, gray_out))
            else:
                gray_in = parts[2]
                bin_out = parts[-1]
                results.append((gray_in, bin_out))
    return results

def main(num_tests=16):
    print("--- Binary <-> Gray Code Conversion Integration ---")

    bin_inputs = [format(random.randint(0, 15), '04b') for _ in range(num_tests)]
    gray_inputs = [format(random.randint(0, 15), '04b') for _ in range(num_tests)]


    print("Running Verilog: binary_to_gray...")
    bin2gray_results = run_verilog_tb(
        "tb_binary_to_gray.v", "binary_to_gray.v", bin_inputs, 'binary')

    print("Running Verilog: gray_to_binary...")
    gray2bin_results = run_verilog_tb(
        "tb_gray_to_binary.v", "gray_to_binary.v", gray_inputs, 'gray')

    csv_rows = [
        ["Input Binary", "Gray from Verilog", "Gray from Python", "Input Gray", "Binary from Verilog", "Binary from Python"]
    ]
    for i in range(num_tests):
        bin_in = bin_inputs[i]
        gray_in = gray_inputs[i]
        gray_from_verilog = bin2gray_results[i][1] if i < len(bin2gray_results) else "ERR"
        gray_from_python = binary_to_gray(bin_in)
        bin_from_verilog = gray2bin_results[i][1] if i < len(gray2bin_results) else "ERR"
        bin_from_python = gray_to_binary(gray_in)
        csv_rows.append([
            bin_in, gray_from_verilog, gray_from_python,
            gray_in, bin_from_verilog, bin_from_python
        ])

    csv_filename = "conversion_results.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_rows)
    print(f"Results written to {csv_filename}\n")


    print("--- Conversion Results ---")
    mismatches = []
    for idx, row in enumerate(csv_rows[1:], 1):
        print(f"Binary: {row[0]} | Gray (Verilog): {row[1]} | Gray (Python): {row[2]} | "
              f"Gray: {row[3]} | Binary (Verilog): {row[4]} | Binary (Python): {row[5]}")
        # Check for mismatches
        if row[1] != row[2]:
            mismatches.append(f"Test {idx}: Binary {row[0]} -> Gray mismatch (Verilog: {row[1]}, Python: {row[2]})")
        if row[4] != row[5]:
            mismatches.append(f"Test {idx}: Gray {row[3]} -> Binary mismatch (Verilog: {row[4]}, Python: {row[5]})")

    print("\n--- Test Case Verification ---")
    if not mismatches:
        print(f"All {num_tests * 2} test cases passed! Verilog and Python outputs match.")
    else:
        print(f"{len(mismatches)} test case(s) failed!")
        for msg in mismatches:
            print(msg)
    print("\nDone.")

if __name__ == "__main__":
    main(num_tests=16)
