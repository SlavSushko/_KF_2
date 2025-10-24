import json
import sys
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Minimal CLI prototype for dependency graph visualization tool.")
    parser.add_argument('--config', default='config.json', help='Path to the JSON configuration file (default: config.json)')
    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f"Error: Configuration file '{args.config}' not found.")
        sys.exit(1)

    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{args.config}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to read configuration file: {str(e)}")
        sys.exit(1)

    required_params = [
        'package_name',
        'repo_url_or_path',
        'repo_mode',
        'graph_file_name',
        'ascii_tree_mode',
        'filter_substring'
    ]

    missing_keys = [key for key in required_params if key not in config]
    if missing_keys:
        print("Error: Missing required configuration parameters:")
        for key in missing_keys:
            print(f" - {key}")
        sys.exit(1)

    errors = []

    if not isinstance(config['package_name'], str) or not config['package_name'].strip():
        errors.append("package_name must be a non-empty string.")

    if not isinstance(config['repo_url_or_path'], str) or not config['repo_url_or_path'].strip():
        errors.append("repo_url_or_path must be a non-empty string.")

    if not isinstance(config['repo_mode'], str) or config['repo_mode'].lower() not in ['url', 'file']:
        errors.append("repo_mode must be either 'url' or 'file'.")

    if not isinstance(config['graph_file_name'], str) or not config['graph_file_name'].strip():
        errors.append("graph_file_name must be a non-empty string.")
    elif not config['graph_file_name'].lower().endswith(('.png', '.jpg', '.svg')):
        print("Warning: graph_file_name should end with a valid image extension (e.g., .png, .jpg, .svg).")

    if not isinstance(config['ascii_tree_mode'], bool):
        errors.append("ascii_tree_mode must be a boolean (true/false).")

    if not isinstance(config['filter_substring'], str):
        errors.append("filter_substring must be a string.")

    if errors:
        print("Error: Configuration validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print("User-configurable parameters:")
    for key in required_params:
        value = config[key]
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()