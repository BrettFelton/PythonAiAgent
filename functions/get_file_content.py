from config import MAX_CHARS

import os


def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        if os.path.commonpath([abs_working_dir, target_path]) != abs_working_dir:
            return f"Error: Cannot list \"{file_path}\" as it is outside the permitted working directory"

        if not os.path.isfile(target_path):
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"

        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += f"[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"

        return file_content_string
   
    except Exception as e:
        return f"Error: {e}"