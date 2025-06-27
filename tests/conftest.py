import os
import sys

# Add the stubs directory so tests use the bundled Flask stub.
stubs_path = os.path.join(os.path.dirname(__file__), 'stubs')
if stubs_path not in sys.path:
    sys.path.insert(0, stubs_path)

# Add the project root to ensure ``localspiral`` imports resolve without
# installing the package.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
