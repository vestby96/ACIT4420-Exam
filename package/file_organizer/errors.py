class FileOrganizerError(Exception):
    """Base class for exceptions in the File Organizer."""

class InvalidDirectoryNameError(FileOrganizerError):
    """Raised when a directory name is invalid."""

class DirectoryNotFoundError(FileOrganizerError):
    """Raised when the specified directory does not exist."""

class PermissionDeniedError(FileOrganizerError):
    """Raised when permission is denied for the directory."""