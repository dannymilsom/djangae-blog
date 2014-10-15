import sys
from os.path import dirname, abspath, join, exists

PROJECT_DIR = dirname(dirname(abspath(__file__)))
SITEPACKAGES_DIR = join(PROJECT_DIR, "sitepackages")
APPENGINE_DIR = join(SITEPACKAGES_DIR, "google_appengine")

def fix_path():
    if exists(APPENGINE_DIR) and APPENGINE_DIR not in sys.path:
        sys.path.insert(1, APPENGINE_DIR)

    if SITEPACKAGES_DIR not in sys.path:
        sys.path.insert(1, SITEPACKAGES_DIR)
