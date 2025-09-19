import random
import subprocess
import os


def binary_to_gray(bin_str):
    """Converts a 4-bit binary string to a Gray code string."""
    val = int(bin_str, 2)
    gray_val = val ^ (val >> 1)
    return format(gray_val, '04b')

def gray_to_binary(gray_str):
    """Converts a 4-bit Gray code string to a binary string."""
    val = int(gray_str, 2)
    mask = val >> 1
    while mask != 0:
        val = val ^ mask
        mask = mask >> 1
    return format(val, '04b')

# --- Main Verification Logic ---

def run_verification(num_tests=20):
    """
    Generates random inputs, runs the Verilog simulation,
    and verifies the output.
    """
    print("--- Starting Verilog Verification ---")
    mismatches = 0
    total_checks = 0

    # 1. Generate random input vectors
    print(f"Generating {num_tests} random 4-bit input vectors...")
    input_vectors = []
    for _ in range(num_tests):
        # Generate a random 4-bit binary number and a random 4-bit gray number
        rand_bin = format(random.randint(0, 15), '04b')
        rand_gray = format(random.randint(0, 15), '04b')
        # Combine them into an 8-bit vector for the testbench
        input_vectors.append(f"{rand_bin}{rand_gray}")

    # Write vectors to file
    with open("input_vectors.txt", "w") as f:
        for vec in input_vectors:
            f.write(f"{vec}\n")
    print("Input vectors written to input_vectors.txt")

    # 2. Run Verilog Simulation
    print("\nRunning Verilog simulation using Icarus Verilog...")
    verilog_files = ["converter.v", "converter_tb.v"]
    compile_cmd = ["iverilog", "-o", "converter_tb"] + verilog_files
    run_cmd = ["vvp", "converter_tb"]

    try:
        # Compile
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
        # Run
        sim_output = subprocess.run(run_cmd, check=True, capture_output=True, text=True)
        print("Simulation completed successfully.")
        print(sim_output.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("\n--- Verilog Simulation FAILED ---")
        print(f"Error during compilation or execution: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return
    except FileNotFoundError:
        print("\n--- Verilog Simulation FAILED ---")
        print("Error: 'iverilog' or 'vvp' not found.")
        print("Please make sure Icarus Verilog is installed and in your system's PATH.")
        return


    # 3. Verify the outputs
    print("\n--- Verifying Simulation Outputs ---")
    try:
        with open("output_vectors.txt", "r") as f:
            sim_outputs = f.readlines()
    except FileNotFoundError:
        print("Error: output_vectors.txt not found. Simulation may have failed.")
        return

    for i, line in enumerate(sim_outputs):
        # Parse inputs and outputs
        original_bin_in = input_vectors[i][0:4]
        original_gray_in = input_vectors[i][4:8]
        parts = line.strip().split()
        if len(parts) != 2:
            continue
        sim_gray_out, sim_bin_out = parts

        # Python's expected results
        expected_gray = binary_to_gray(original_bin_in)
        expected_bin = gray_to_binary(original_gray_in)

        # Check Binary -> Gray conversion
        total_checks += 1
        if sim_gray_out != expected_gray:
            mismatches += 1
            print(f"MISMATCH (Bin->Gray) on test case {i+1}:")
            print(f"  Input Binary:   {original_bin_in}")
            print(f"  Verilog Output: {sim_gray_out}")
            print(f"  Python Expected:  {expected_gray}\n")

        # Check Gray -> Binary conversion
        total_checks += 1
        if sim_bin_out != expected_bin:
            mismatches += 1
            print(f"MISMATCH (Gray->Bin) on test case {i+1}:")
            print(f"  Input Gray:     {original_gray_in}")
            print(f"  Verilog Output: {sim_bin_out}")
            print(f"  Python Expected:  {expected_bin}\n")

    # 4. Report final results
    print("\n--- Verification Summary ---")
    if mismatches == 0:
        print(f"Success! All {total_checks} checks passed across {num_tests} test cases.")
    else:
        print(f"❌ Failure! Found {mismatches} mismatches out of {total_checks} checks.")

    # Clean up generated files
    print("\nCleaning up generated files...")
    for f in ["input_vectors.txt", "output_vectors.txt", "converter_tb"]:
        if os.path.exists(f):
            os.remove(f)
    print("Cleanup complete.")


if __name__ == "__main__":
    # You can change the number of random tests here
    run_verification(num_tests=25)
