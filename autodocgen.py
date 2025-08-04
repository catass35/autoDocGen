#### @title: autoDocGen v1.0
"""This progamm generates documentation from comments automatically"""

### @section: Import
import sys
import os
import re
import json

### @section: Global variables
## @var: dictionnary of supported extensions
SUPPORTED_EXTENSIONS = {'.txt', '.csv', '.json', '.xml', '.yaml', '.yml', '.md', '.py'}

### @section: Function definition

## @function: is_supported_file(file_path)
# @param: input file path
# @return: boolean
# @describtion: check whether the given file path extension is a supported file extension
def is_supported_file(file_path):
    """Check if the file extension is in the list of supported file extensions"""
    _, ext = os.path.splitext(file_path)
    return ext.lower() in SUPPORTED_EXTENSIONS

## @function: load_config(config_path)
# @param: config file path
# @return: object
# @describtion: if configuration file exists, load the configuration else return error
def load_config(config_path):
    """Return an object from load configuration of json file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_path}")
        return None
    except PermissionError:
        print(f"❌ Permission denied when accessing: {config_path}")
        return None
    except OSError as e:
        print(f"❌ OS error while accessing config: {e}")
        return None

## @function: extract_lines_with_patterns(file_path, patterns)
# @param: input file path, configuration
# @return: list
# @describtion: append a list with all lines maching the patterns from loaded configuration
def extract_lines_with_patterns(file_path, patterns):
    """Put all occurrences of matching patterns into a list"""
    results = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for pattern_def in patterns:
                match = re.match(pattern_def["pattern"], line)
                if match:
                    transformed = re.sub(pattern_def["pattern"],
                                         pattern_def["transform"],
                                         line).strip()
                    results.append(transformed)
                    break  # Stop checking other patterns for this line
    return results

### @section: Main
def main():
    """main section of the script"""
    if len(sys.argv) != 4:
        print("Usage: python autodocgen.py <input_file> <output_file> <config_file>")
        sys.exit(1)

    input_path, output_path, config_path = sys.argv[1], sys.argv[2], sys.argv[3]

    # @Step 1: Input file must exist
    if not os.path.isfile(input_path):
        print(f"❌ Input file '{input_path}' does not exist.")
        sys.exit(1)

    # @Step 2: Output file must not already exist
    if os.path.exists(output_path):
        print(f"❌ Output file '{output_path}' already exists.")
        sys.exit(1)

    # @Step 3: Config file must exist
    if not os.path.isfile(config_path):
        print(f"❌ Config file '{config_path}' does not exist.")
        sys.exit(1)

    # @Step 4: Input file must be a supported file type
    if not is_supported_file(input_path):
        print(f"❌ Unsupported file extension for '{input_path}'.")
        sys.exit(1)

    # @Step 5: Load matching patterns from config
    config_patterns = load_config(config_path)

    # @Step 6: Extract matching lines with transformations
    extracted_lines = extract_lines_with_patterns(input_path, config_patterns)

    # @Step 7: Write output
    if extracted_lines:
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write('\n'.join(extracted_lines))
        print(f"✅ Extracted {len(extracted_lines)} line(s) written to '{output_path}'.")
    else:
        print("⚠️ No matching lines found.")

if __name__ == "__main__":
    main()
