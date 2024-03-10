import os
import sys

package_directory = os.path.dirname(__file__)

if package_directory not in sys.path:
    sys.path.append(package_directory)
    