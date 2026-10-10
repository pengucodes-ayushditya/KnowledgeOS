"""

Application-wide constants.

Only values that never change across environments should live here.

Configuration values (database URLs, model names, dimensions,
directories, etc.) belong in app.core.config.
"""

# The existing initial database migration declares Vector(dim=1024).
# Changing this persisted column width requires an explicit schema migration.
DEFAULT_EMBEDDING_DIMENSION = 1024
