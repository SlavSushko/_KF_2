import json
import sys
import argparse
import os
import urllib.request
import gzip
import re


def get_packages_data(url_or_path, mode):
    try:
        if mode.lower() == 'url':
            with urllib.request.urlopen(url_or_path) as response:
                data = response.read()
        elif mode.lower() == 'file':
            with open(url_or_path, 'rb') as f:
                data = f.read()
        else:
            raise ValueError("Invalid repo_mode.")

        if url_or_path.lower().endswith('.gz'):
            data = gzip.decompress(data)

        return data.decode('utf-8')
    except urllib.error.URLError as e:
        print(f"Error: Failed to download from URL: {str(e)}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{url_or_path}' not found.")
        sys.exit(1)
    except gzip.BadGzipFile:
        print("Error: Invalid gzip file.")
        sys.exit(1)
    except UnicodeDecodeError:
        print("Error: Failed to decode file content as UTF-8.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected error while fetching data: {str(e)}")
        sys.exit(1)


def parse_packages(text):
    packages = {}
    current = {}
    for line in text.splitlines():
        if not line.strip():
            if current:
                pkg = current.get('Package')
                if pkg:
                    packages[pkg] = current
                current = {}
            continue
        if ':' in line:
            key, value = line.split(':', 1)
            current[key.strip()] = value.strip()
    if current:
        pkg = current.get('Package')
        if pkg:
            packages[pkg] = current
    return packages


def parse_depends(depends_str):
    if not depends_str:
        return []
    deps = []
    for part in depends_str.split(','):
        part = part.strip()
        alts = [alt.strip() for alt in part.split('|')]
        for alt in alts:
            match = re.match(r'([\w\-+.]+)', alt)
            if match:
                deps.append(match.group(1))
    return sorted(set(deps))


def main():
    parser = argparse.ArgumentParser(
        description="Dependency graph visualization tool - Stage 2: Fetch and display direct dependencies.")
    parser.add_argument('--config', default='config.json',
                        help='Path to the JSON configuration file (default: config.json)')
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

    packages_text = get_packages_data(config['repo_url_or_path'], config['repo_mode'])

    packages = parse_packages(packages_text)

    if config['package_name'] not in packages:
        print(f"Error: Package '{config['package_name']}' not found in the repository.")
        sys.exit(1)

    depends_str = packages[config['package_name']].get('Depends', '')

    direct_deps = parse_depends(depends_str)

    print(f"Direct dependencies of '{config['package_name']}':")
    if direct_deps:
        for dep in direct_deps:
            print(dep)
    else:
        print("No direct dependencies found.")


if __name__ == "__main__":
    main()