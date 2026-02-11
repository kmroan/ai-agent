import os, subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if ".py" not in file_path:
            return f'Error: "{file_path}" is not a Python file'
        if valid_target_file == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        command = ["python", target_file]
        if args:
            command.extend([args])
        cmd = subprocess.run(command,text=True,capture_output=True,timeout=30)
        res = ""
        if cmd.returncode  > 0:
            res +=  f"Process exited with code {cmd.returncode}"
        if cmd.stdout == None or cmd.stderr == None:
            res += "No output produced"
        res += f"STDOUT:{cmd.stdout}\nSTDERR:{cmd.stderr}"
        return res
    except Exception as e:
        return f"Error: {e}"
