"""
Application Constants
---------------------

This file contains all configuration constants
used throughout the AI PDF Chatbot project.
"""

# ==========================================================
# PDF SETTINGS
# ==========================================================

MAX_FILE_SIZE = 20 * 1024 * 1024      # 20 MB
ALLOWED_FILE_TYPES = ["pdf"]

# ==========================================================
# CHUNKING SETTINGS
# ==========================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ==========================================================
# RETRIEVAL SETTINGS
# ==========================================================

TOP_K_RESULTS = 5

# ==========================================================
# UPLOAD SETTINGS
# ==========================================================

UPLOAD_FOLDER = "data/uploads"
