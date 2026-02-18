import os
import config
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Print content of the specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File whose contents should be listed, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if valid_target_file == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as file:
            c = file.read(config.MAX_CHARS)
            if file.read(1):
                c += f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
        return c
    except Exception as e:
        return f"Error: {e}"
