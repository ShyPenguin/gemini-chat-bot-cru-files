import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "This writes or overwrites the content of the given file."
        "Creates the parent directory of the file if it doesn't exist"
        "This also creates the file if the file doesn't exist"
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "This is the file referred from the function's description"
                    "The file_path must be a relative path and must not escape the working directory. "
                    "Relative path to the file (e.g., 'src/index.js', 'README.md'). "
                    "Must point to a file inside the working directory."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description=(
                    "A string that is used to overwrite or updates the file"
                ),
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    try :
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_file_path = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    