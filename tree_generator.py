import argparse
from pathlib import Path

def generate_tree(dir_path: Path, prefix: str = ""):
    """
    Recursively generates a visual tree structure of a directory.
    """
    # Folders/files to exclude from the output
    ignore_list = {
        '.git', '__pycache__', 'dist', 'build', 
        '.idea', '.vscode', '.venv', 'node_modules', 
        '.DS_Store', '__init__.py'
    }
    
    # Filter and sort items: Directories first, then files alphabetically
    try:
        items = sorted(
            [p for p in dir_path.iterdir() if p.name not in ignore_list], 
            key=lambda x: (x.is_file(), x.name.lower())
        )
    except PermissionError:
        return

    # Create tree visual pointers
    pointers = ["├── "] * (len(items) - 1) + ["└── "] if items else []
    
    for pointer, item in zip(pointers, items):
        print(f"{prefix}{pointer}{item.name}")
        if item.is_dir():
            # Recursive call for subdirectories with adjusted indentation
            extension = "│   " if pointer == "├── " else "    "
            generate_tree(item, prefix=prefix + extension)

def main():
    """
    CLI entry point for the directory tree generator.
    """
    parser = argparse.ArgumentParser(description="A lightweight CLI tool to generate directory tree structures.")
    parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="Target directory path (default: current directory)"
    )
    
    args = parser.parse_args()
    target_path = Path(args.path).resolve()
    
    if not target_path.is_dir():
        print(f"Error: '{args.path}' is not a valid directory.")
        return

    print(f"\n{target_path.name}/")
    generate_tree(target_path)

if __name__ == "__main__":
    main()
