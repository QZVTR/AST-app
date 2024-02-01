import os
import random

def generate_program(iteration):
    program_name = f"program_v{iteration}.py"
    with open(program_name, "w") as file:
        file.write("# Iteration {}\n".format(iteration))
        file.write("import random\n")
        file.write("def main():\n")
        file.write("    nums = [random.randint(1, 100) for _ in range(10)]\n")
        file.write("    print('Original list:', nums)\n")
        file.write("    nums.sort()\n")
        file.write("    print('Sorted list:', nums)\n")
        file.write("if __name__ == '__main__':\n")
        file.write("    main()\n")

def modify_program(iteration):
    if iteration == 0:
        generate_program(1)
        return

    with open(f"program_v{iteration}.py", "r") as original_file:
        lines = original_file.readlines()

    # Make slight modifications
    modification = random.choice(["comment", "reorder"])
    modified_lines = lines[:]
    if modification == "comment":
        line_number = random.randint(1, len(lines) - 1)
        modified_lines.insert(line_number, "# This is a new comment added in iteration {}\n".format(iteration))
    elif modification == "reorder":
        # Preserve import statements and function definitions
        essential_lines = [line for line in modified_lines if line.startswith(("import", "def"))]
        modified_lines = [line for line in modified_lines if line not in essential_lines]
        random.shuffle(modified_lines)
        modified_lines = essential_lines + modified_lines

    modified_program_name = f"program_v{iteration + 1}.py"
    with open(modified_program_name, "w") as modified_file:
        modified_file.writelines(modified_lines)

# Start modification process
for i in range(0, 11):
    modify_program(i)

    # Execute the modified program
    # os.system(f"python program_v{i}.py")
