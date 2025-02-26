class DatabaseError(Exception):
    """Raised when a database fails to process the query."""
    pass

class MovieNotFoundError(Exception):
    """Raised when a requested resource is not found in the database."""
    pass