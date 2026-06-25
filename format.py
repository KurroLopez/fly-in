"""Text formatting using ANSI escape codes."""
CLEAR: str = '\033[0m'  # Remove all text formatting.
BOLD: str = '\033[1m'  # Bold text formatting.
ERROR: str = '\033[1;91m'  # Red text formatting for errors.
WARNING: str = '\033[93m'  # Yellow text formatting for warnings.
TAB: str = '\t'  # Tab character for indentation.
