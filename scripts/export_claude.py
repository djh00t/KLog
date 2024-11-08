#!/usr/bin/env python3
"""
claude_export.py: A script to export and concatenate all files from specified directories.

This script performs the following tasks:
1. Finds all files in the specified directories, excluding certain directories.
2. Creates a 'data/claude_export' directory if it doesn't exist.
3. Parses .gitignore and applies its rules.
4. Filters files based on .gitignore rules and static_exclude list.
5. Concatenates final list of files into a single output file with customizable delimiters.
6. Logs statistics about the process.

Usage:
    python claude_export.py [-d] [--project-name PROJECT_NAME] [--dir DIR]... [--delimiter DELIMITER]

Options:
    -d, --debug            Enable debug mode for verbose output.
    --project-name NAME    Specify the project name for the output file.
    --dir DIR              Specify root directories to search (can be used multiple times).
    --delimiter DELIMITER  Specify the delimiter to use between files (default: "# {file_path}").
"""

import os
import argparse
import subprocess
from datetime import datetime
import fnmatch
from typing import List
import shlex
import logging
from collections import Counter

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directories to exclude when searching for files and .gitignore files
EXCLUDE_DIRS = {
    '.git',
    '.pytest_cache',
    '__pycache__',
    'node_modules',
    'venv',
    '.venv',
}

# Static exclude patterns
STATIC_EXCLUDE = [
    ".gitignore",
    "*__pycache__*",
    "*data/claude_export*",
    "*.git",
    "*.pytest_cache",
    ".venv/",
    "*archive*",
    "*chroma.db",
    "*.aider*",
    "*.DS_Store",
    "*.python-version",
    "**.pyc",
]

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Export and concatenate files from specified directories.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--project-name", default="project", help="Specify the project name")
    parser.add_argument("--dir", action="append", default=[], help="Specify root directories to search (can be used multiple times)")
    parser.add_argument("--delimiter", default="# {file_path}", help="Specify the delimiter to use between files")
    return parser.parse_args()

def create_export_directory() -> None:
    """Create the 'data/claude_export' directory if it doesn't exist."""
    os.makedirs("data/claude_export", exist_ok=True)

def should_exclude_dir(dir_name: str) -> bool:
    """Check if a directory should be excluded from processing."""
    return any(excluded in dir_name.split(os.sep) for excluded in EXCLUDE_DIRS)

def find_all_files(root_dirs: List[str]) -> List[str]:
    """Find all files in the specified directories, excluding certain directories."""
    file_names = []
    for root_dir in root_dirs:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Exclude certain directories
            dirnames[:] = [d for d in dirnames if not should_exclude_dir(os.path.join(dirpath, d))]
            
            for filename in filenames:
                relative_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
                file_names.append(relative_path)
    return file_names

def read_gitignore_with_lines(root_dirs: List[str]) -> List[tuple]:
    """Read all .gitignore files in the given directories and return their contents as a list of (pattern, source, line_number) tuples."""
    gitignore_patterns = []
    for root_dir in root_dirs:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Exclude certain directories
            dirnames[:] = [d for d in dirnames if not should_exclude_dir(os.path.join(dirpath, d))]
            
            if '.gitignore' in filenames:
                gitignore_path = os.path.join(dirpath, '.gitignore')
                with open(gitignore_path, 'r') as f:
                    for line_number, line in enumerate(f, 1):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            gitignore_patterns.append((line, gitignore_path, line_number))
    return gitignore_patterns

def filter_files(file_names: List[str], exclude_patterns: List[str], gitignore_patterns: List[tuple]) -> List[str]:
    """Filter files based on exclude patterns and gitignore patterns."""
    combined_patterns = [(pattern, "static_exclude", 0) for pattern in exclude_patterns] + gitignore_patterns
    filtered_files = []
    excluded_files = []
    pattern_matches = Counter()

    for file in file_names:
        excluded = False
        for pattern, source, line_number in combined_patterns:
            if fnmatch.fnmatch(file, pattern):
                excluded = True
                pattern_matches[(pattern, source, line_number)] += 1
                logging.debug(f"Excluded file: {file} (matched pattern: {pattern}, source: {source}, line: {line_number})")
                break
        
        if excluded:
            excluded_files.append(file)
        else:
            filtered_files.append(file)
    
    logging.info(f"Total files before filtering: {len(file_names)}")
    logging.info(f"Total files after filtering: {len(filtered_files)}")
    
    if len(filtered_files) == 0:
        logging.warning("All files were excluded. Check your .gitignore and static_exclude patterns.")
    
    logging.info("Pattern match counts:")
    for (pattern, source, line_number), count in pattern_matches.most_common():
        if count > 0:
            if source == "static_exclude":
                logging.info(f"  - {pattern}: {count} file(s) (from static_exclude)")
            else:
                logging.info(f"  - {pattern}: {count} file(s) (from {source}, line {line_number})")
    
    return filtered_files

def run_tree_command(root_dir: str, exclude_patterns: List[str]) -> str:
    """Run the tree command with exclude patterns and return the output."""
    ignore_args = [f"-I '{pattern}'" for pattern in exclude_patterns if pattern.strip()]

    cmd = f"tree {root_dir} {' '.join(ignore_args)}"
    result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    return result.stdout

def concatenate_files(files: List[str], output_file: str, root_dirs: List[str], debug: bool, delimiter: str) -> int:
    """Concatenate the contents of the given files into a single output file."""
    included_files = []
    excluded_files = []

    logging.info(f"Concatenating files into {output_file}...")
    logging.info(f"Root directories: {root_dirs}")
    logging.info(f"Files to concatenate: {len(files)}")
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        # Add tree command output at the top of the file
        for root_dir in root_dirs:
            tree_output = run_tree_command(root_dir, STATIC_EXCLUDE)
            outfile.write(f"Tree structure for {root_dir}:\n")
            outfile.write(tree_output)
            outfile.write("\n\n")

        # Concatenate file contents
        for file in files:
            # Try to find the file in one of the root directories
            full_path = None
            for root_dir in root_dirs:
                potential_path = os.path.join(root_dir, file)
                if os.path.exists(potential_path):
                    full_path = potential_path
                    break

            if full_path:
                # Write the delimiter with a newline before and after
                outfile.write(f"\n{delimiter.format(file_path=file)}\n\n")
                try:
                    with open(full_path, "r", encoding="utf-8") as infile:
                        file_content = infile.read()
                        outfile.write(file_content)
                    outfile.write("\n")
                    included_files.append(file)
                except Exception as e:
                    logging.error(f"Error reading file {file}: {e}")
                    excluded_files.append(file)
            else:
                excluded_files.append(file)

    if debug:
        logging.debug(f"Included files: {included_files}")
        logging.debug(f"Excluded files: {excluded_files}")

    return len(included_files)

def print_stats(total_files: int, files_after_filtering: int, files_in_output: int) -> None:
    """Print statistics about the file processing."""
    logging.info("\nStatistics:")
    logging.info(f"{'-' * 40}")
    logging.info(f"Total Files: {total_files}")
    logging.info(f"Files after filtering: {files_after_filtering}")
    logging.info(f"Files in output file: {files_in_output}")
    logging.info(f"{'-' * 40}\n")

def main() -> None:
    # Parse command-line arguments
    args = parse_arguments()

    # Set debug flag and configure logging
    debug = args.debug
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logging.info(f"Debug mode: {debug}")

    # Extract command-line arguments
    project_name = args.project_name
    logging.info(f"Project name: {project_name}")
    
    root_dirs = args.dir if args.dir else [os.getcwd()]
    logging.info(f"Root directories: {root_dirs}")

    delimiter = args.delimiter
    logging.info(f"File delimiter: {delimiter}")

    # Create export directory
    create_export_directory()

    # Find all files in the specified directories
    file_names = find_all_files(root_dirs)
    total_files = len(file_names)
    logging.info(f"Total files found: {total_files}")

    # Read .gitignore files and extract patterns
    gitignore_patterns = read_gitignore_with_lines(root_dirs)
    logging.info(f"Total .gitignore patterns: {len(gitignore_patterns)}")

    # Filter out files matching .gitignore patterns and static_exclude
    final_files = filter_files(file_names, STATIC_EXCLUDE, gitignore_patterns)

    if len(final_files) == 0:
        logging.error("No files remained after filtering. Exiting.")
        return

     # Concatenate files into a single output file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"data/claude_export/{timestamp}_{project_name}_all_code.txt"
    files_in_output = concatenate_files(final_files, output_file, root_dirs, debug, delimiter)


    # Print statistics
    print_stats(total_files, len(final_files), files_in_output)

    logging.info(f"\nOutput file created: {output_file}")

if __name__ == "__main__":
    main()