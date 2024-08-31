from django.core.exceptions import ValidationError

# For testing model validation
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 10  # 10mb

def validate_image_size(value):
    if value.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError(_('Image size must be less than 10MB.'))