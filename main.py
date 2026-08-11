import os
import subprocess

def get_cpu_usage():
    """Gets CPU usage on Windows, handling inconsistent whitespace."""
    command = "wmic cpu get loadpercentage"
    output = subprocess.check_output(command, shell=True, text=True)
    lines = [line for line in output.strip().split('\n') if line.strip()]
    return lines[1].strip()

def get_memory_usage():
    """Gets memory usage percentage on Windows, handling inconsistent whitespace."""
    command = "wmic OS get FreePhysicalMemory,TotalVisibleMemorySize"
    output = subprocess.check_output(command, shell=True, text=True)
    lines = [line for line in output.strip().split('\n') if line.strip()]
    parts = lines[1].split()
    free_mem_kb = int(parts[0])
    total_mem_kb = int(parts[1])
    used_mem_kb = total_mem_kb - free_mem_kb
    usage_percent = (used_mem_kb / total_mem_kb) * 100
    return f"{usage_percent:.2f}"

def run_ai_ask(query_parts):
    """Simulates an AI understanding a natural language query."""
    query = " ".join(query_parts).lower()
    print(f"[AI] Processing your request: '{query}'...")
    if "create" in query and "folder" in query:
        try:
            name_index = -1
            if "named" in query_parts:
                name_index = query_parts.index("named") + 1
            elif "folder" in query_parts:
                name_index = query_parts.index("folder") + 1
            folder_name = query_parts[name_index]
            print("[AI] Understood. I will run the following command:")
            print(f"mkdir {folder_name}")
            os.mkdir(folder_name)
            print(f"Directory '{folder_name}' created.")
        except (ValueError, IndexError):
            print("[AI] I understood you want to create a folder, but I couldn't figure out the name.")
    else:
        print("[AI] I'm sorry, I don't understand that request. My capabilities are limited in this demo.")

def print_help():
    """Prints a formatted help message for all commands."""
    print("\n--- msh (Modi Shell) Help ---")
    print("  ls [path]      - Lists files and directories.")
    print("  cd <directory>   - Changes the current directory.")
    print("  pwd              - Shows the current working directory.")
    print("  mkdir <name>     - Creates a new directory.")
    print("  rm <name>        - Removes a file or empty directory.")
    print("  dashboard        - Displays system CPU and Memory usage.")
    print("  modi <query>     - Asks the AI to perform a task (e.g., 'modi create folder test').")
    print("  help             - Shows this help message.")
    print("  exit             - Exits the shell.")
    print("--------------------------------\n")

def run_pwd():
    """Prints the current working directory."""
    print(os.getcwd())

def run_ls(path="."):
    """Lists contents of the specified path."""
    for entry in os.listdir(path):
        print(entry)

def run_cd(path):
    """Changes the current working directory."""
    os.chdir(path)

def run_mkdir(dirname):
    """Creates a new directory."""
    os.mkdir(dirname)
    print(f"Directory '{dirname}' created.")

def run_rm(target):
    """Removes a file or an empty directory."""
    if os.path.isfile(target):
        os.remove(target)
        print(f"File '{target}' removed.")
    elif os.path.isdir(target):
        os.rmdir(target)
        print(f"Directory '{target}' removed.")

# --- Main Shell Logic ---
if __name__ == "__main__":
    while True:
        prompt = f"{os.getcwd()}> "
        command_input = input(prompt)
        parts = command_input.split()
        if not parts:
            continue
        command = parts[0].lower()
        args = parts[1:]
        try:
            if command == "help":
                print_help()
            elif command == "pwd":
                run_pwd()
            elif command == "ls":
                run_ls(args[0] if args else ".")
            elif command == "cd":
                run_cd(args[0]) if args else print("cd: missing operand")
            elif command == "mkdir":
                run_mkdir(args[0]) if args else print("mkdir: missing operand")
            elif command == "rm":
                run_rm(args[0]) if args else print("rm: missing operand")
            elif command == "dashboard":
                cpu = get_cpu_usage()
                mem = get_memory_usage()
                print("--- System Dashboard ---")
                print(f"CPU Usage:    {cpu}%")
                print(f"Memory Usage: {mem}%")
                print("----------------------")
            elif command == "modi":
                run_ai_ask(args) if args else print("modi: missing query")
            elif command == "exit":
                print("Exiting msh...")
                break
            else:
                print(f"msh: command not found: {command}")
        except Exception as e:
            print(f"An error occurred: {e}")
