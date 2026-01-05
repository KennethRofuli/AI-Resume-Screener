"""
Security middleware and utilities for API protection
"""
from fastapi import Request, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from typing import Optional
from pathlib import Path
import logging

# Try to import magic, but make it optional for Windows compatibility
try:
    import magic
    MAGIC_AVAILABLE = True
except (ImportError, OSError):
    MAGIC_AVAILABLE = False
    logging.warning("python-magic not available. MIME type validation will be skipped.")

from config import config

logger = logging.getLogger(__name__)

# API Key header scheme
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """
    Verify API key from header
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        Validated API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not config.REQUIRE_API_KEY:
        return "no-auth-required"
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Please provide X-API-Key header."
        )
    
    if not config.is_valid_api_key(api_key):
        logger.warning(f"Invalid API key attempt: {api_key[:8]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return api_key


async def validate_file_upload(
    file_content: bytes,
    filename: str,
    max_size: Optional[int] = None
) -> None:
    """
    Validate uploaded file for security
    
    Args:
        file_content: File content bytes
        filename: Original filename
        max_size: Maximum file size in bytes (defaults to config)
        
    Raises:
        HTTPException: If file validation fails
    """
    max_size = max_size or config.MAX_FILE_SIZE_BYTES
    
    # Check file size
    if len(file_content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {config.MAX_FILE_SIZE_MB}MB"
        )
    
    # Check file extension
    file_ext = Path(filename).suffix.lower()
    if file_ext not in config.ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(config.ALLOWED_FILE_EXTENSIONS)}"
        )
    
    # Check if file is empty
    if len(file_content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )
    
    # Verify MIME type using python-magic (if available)
    if MAGIC_AVAILABLE:
        try:
            mime = magic.from_buffer(file_content, mime=True)
            if mime not in config.ALLOWED_MIME_TYPES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid file type. Detected: {mime}. File extension and content must match."
                )
        except Exception as e:
            logger.warning(f"MIME type detection failed: {e}")
            # Continue if magic fails, extension check is still valid
    else:
        logger.debug("MIME type validation skipped (python-magic not available)")


def validate_text_input(text: str, field_name: str = "text") -> None:
    """
    Validate text input length and content
    
    Args:
        text: Text to validate
        field_name: Name of the field for error messages
        
    Raises:
        HTTPException: If validation fails
    """
    if not text or not text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field_name} cannot be empty"
        )
    
    if len(text) > config.MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"{field_name} too long. Maximum {config.MAX_TEXT_LENGTH} characters"
        )


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove any directory path components
    filename = Path(filename).name
    
    # Remove any non-alphanumeric characters except dots, dashes, underscores
    safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_")
    filename = "".join(c if c in safe_chars else "_" for c in filename)
    
    # Limit filename length
    if len(filename) > 255:
        name_part = filename[:200]
        ext_part = Path(filename).suffix[-50:]
        filename = name_part + ext_part
    
    return filename


async def validate_batch_size(files_count: int) -> None:
    """
    Validate batch analysis size
    
    Args:
        files_count: Number of files in batch
        
    Raises:
        HTTPException: If batch size exceeds limit
    """
    if files_count > config.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Batch size too large. Maximum {config.MAX_BATCH_SIZE} files allowed"
        )
    
    if files_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided"
        )
