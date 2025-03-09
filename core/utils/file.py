from PIL import Image

class ImageFile:
    
    @staticmethod
    def reduce_image_quality(input_image_path, output_image_path, quality=30,target_format = 'webp'):
        """
        Reduces the image quality and saves the new image.

        Args:
        - input_image_path (str): The path to the input image.
        - output_image_path (str): The path to save the reduced quality image.
        - quality (int): The quality of the saved image (0 to 100, default is 50).
        - target_format (str): Desired output format ('jpeg', 'png', 'webp').

        # Example usage:
        ImageFile.reduce_image_quality('input_image.jpg', 'output_image.jpg', quality=30)  # Adjust quality from 0 to 100
        """
        # Open the image
        img = Image.open(input_image_path)
        
        # Check if the image format is JPEG or other supported formats for quality reduction
        if target_format == 'jpeg':
            img.convert("RGB").save(output_image_path, format='JPEG', quality=quality)
        elif target_format == 'webp':
            # WebP is the most efficient for web images
            img.convert("RGB").save(output_image_path, format='WebP', quality=quality, method=6)
        elif target_format == 'png':
            # PNG doesn't support quality, but we can still optimize the file
            img.save(output_image_path, format='PNG', optimize=True)
        else:
            raise ValueError("Unsupported format: Please choose 'jpeg', 'webp', or 'png'.")
        
        
        print(f"Image saved with reduced quality at: {output_image_path}")


