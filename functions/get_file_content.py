import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Reads and returns the content of a file located within the working directory. "
        "If the file is too large, the content will be truncated."
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
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_file_path = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"