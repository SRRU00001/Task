from PIL import Image
import io
import os
from app.config import settings
import logging

logger = logging.getLogger(__name__)


async def crop_and_save_image(image_file, filename: str) -> str:
    """
    Crop image to specified ratio (450x350) and save it.
    
    Args:
        image_file: Uploaded file object
        filename: Original filename
        
    Returns:
        str: Relative URL path to saved image
    """
    try:
        # Read image file
        image_bytes = await image_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Get original dimensions
        original_width, original_height = image.size
        
        # Calculate target aspect ratio
        target_ratio = settings.IMAGE_CROP_WIDTH / settings.IMAGE_CROP_HEIGHT
        
        # Calculate crop dimensions maintaining aspect ratio
        if original_width / original_height > target_ratio:
            # Image is wider than target ratio
            new_height = original_height
            new_width = int(original_height * target_ratio)
            left = (original_width - new_width) // 2
            top = 0
            right = left + new_width
            bottom = original_height
        else:
            # Image is taller than target ratio
            new_width = original_width
            new_height = int(original_width / target_ratio)
            left = 0
            top = (original_height - new_height) // 2
            right = original_width
            bottom = top + new_height
        
        # Crop image
        cropped_image = image.crop((left, top, right, bottom))
        
        # Resize to target dimensions
        resized_image = cropped_image.resize(
            (settings.IMAGE_CROP_WIDTH, settings.IMAGE_CROP_HEIGHT),
            Image.Resampling.LANCZOS
        )
        
        # Generate unique filename
        import uuid
        file_extension = os.path.splitext(filename)[1] or ".jpg"
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Ensure upload directory exists
        upload_dir = settings.UPLOAD_DIR
        if not os.path.isabs(upload_dir):
            # If relative path, make it relative to app directory
            import pathlib
            app_dir = pathlib.Path(__file__).parent.parent
            upload_dir = str(app_dir / upload_dir)
        
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save image
        file_path = os.path.join(upload_dir, unique_filename)
        resized_image.save(file_path, quality=85, optimize=True)
        
        # Return relative URL path
        return f"/static/uploads/{unique_filename}"
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise Exception(f"Failed to process image: {str(e)}")

