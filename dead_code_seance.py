#!/usr/bin/env python3
"""Dead Code Séance - Summon the ghosts of unused functions."""

import ast
import os
import sys
from pathlib import Path


def find_python_files(root_dir):
    """Find Python files like a truffle pig finds truffles."""
    return [str(p) for p in Path(root_dir).rglob('*.py')]


def extract_definitions(filepath):
    """Extract function/class names - the potential ghosts in our machine."""
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            return []  # Some ghosts are too spooky to parse
    
    definitions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            definitions.append((node.name, 'function', filepath))
        elif isinstance(node, ast.ClassDef):
            definitions.append((node.name, 'class', filepath))
    return definitions


def search_references(definitions, files):
    """Hunt for references like a detective with too much coffee."""
    used = set()
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for name, _, _ in definitions:
                if name in content:
                    # Count occurrences, excluding the definition itself
                    lines = content.split('\n')
                    for line in lines:
                        if name in line and f'def {name}' not in line and f'class {name}' not in line:
                            used.add(name)
    return used


def main():
    """Main séance - light the candles and call the spirits."""
    if len(sys.argv) != 2:
        print('Usage: python dead_code_seance.py <directory>')
        print('Example: python dead_code_seance.py ./src')
        sys.exit(1)
    
    root_dir = sys.argv[1]
    if not os.path.isdir(root_dir):
        print(f'Error: {root_dir} is not a directory')
        sys.exit(1)
    
    print(f'\n🔮 Conducting séance in {root_dir}...\n')
    
    files = find_python_files(root_dir)
    print(f'Found {len(files)} Python files (potential haunted houses)')
    
    all_defs = []
    for filepath in files:
        all_defs.extend(extract_definitions(filepath))
    
    print(f'Found {len(all_defs)} definitions (potential ghosts)')
    
    used = search_references(all_defs, files)
    
    print(f'\n👻 GHOSTS (unused code):')
    print('=' * 40)
    ghost_count = 0
    for name, typ, filepath in all_defs:
        if name not in used:
            print(f'{typ:10} {name:30} in {filepath}')
            ghost_count += 1
    
    if ghost_count == 0:
        print('No ghosts found! The codebase is... alive? 🧟')
    else:
        print(f'\nTotal ghosts: {ghost_count} (rest in peace)')


if __name__ == '__main__':
    main()
