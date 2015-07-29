"""Version Module

So we only have to maintain version information in one place!
"""

version_info = (0, 0, 1, "dev")  # (major, minor, patch, dev?)
version = (
    ".".join(map(str, version_info))
    if version_info[-1] != "dev"
    else "dev"
)
