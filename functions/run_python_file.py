import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file the working directory with optional arguments. "
        "The file must be a valid .py file and must not be outside the working directory. "
        "Returns the output of the execution (stdout/stderr) or an error if execution fails "
        "or times out."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Relative path to the Python file (e.g., 'scripts/main.py'). "
                    "Must point to a .py file inside the working directory."
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments for the Python script.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single command-line argument."
                ),
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try :
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_file_path = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if abs_file_path[-3:] != '.py':
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", abs_file_path]
        if args:
            command.extend(args)

        result_subprocess = subprocess.run(command, capture_output=True, text=True, timeout=30)

        result_string = ""
        if result_subprocess.returncode != 0:
            result_string += "Process exited with code X\n"
        if result_subprocess.stdout:
            result_string += f"STDOUT:{result_subprocess.stdout}\n"
        elif result_subprocess.stderr:
            result_string += f"STDERR:{result_subprocess.stderr}\n"
        else:
            result_string += "No output produced"

        return result_string
            
    except Exception as e:
        return f"Error: executing Python file: {e}"