import qrcode
import os
from io import BytesIO
import base64

class QRCodeGenerator:
    """Utility class for generating and managing QR codes"""
    
    def __init__(self, qr_folder='static/qrcodes'):
        self.qr_folder = qr_folder
        self._ensure_qr_folder()
    
    def _ensure_qr_folder(self):
        """Ensure the QR codes folder exists"""
        if not os.path.exists(self.qr_folder):
            os.makedirs(self.qr_folder)
    
    def generate_qr_code(self, teacher_unique_id, teacher_name):
        """
        Generate QR code for a teacher
        
        Args:
            teacher_unique_id (str): Unique identifier for the teacher
            teacher_name (str): Teacher's name for display purposes
            
        Returns:
            tuple: (qr_filename, qr_data_url)
        """
        # Create QR code data
        qr_data = f"TEACHER:{teacher_unique_id}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Save to file
        filename = f"teacher_{teacher_unique_id}.png"
        filepath = os.path.join(self.qr_folder, filename)
        qr_image.save(filepath)
        
        # Generate data URL for web display
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        qr_data_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
        
        return filename, qr_data_url
    
    def get_qr_code_path(self, teacher_unique_id):
        """Get the file path for a teacher's QR code"""
        filename = f"teacher_{teacher_unique_id}.png"
        return os.path.join(self.qr_folder, filename)
    
    def delete_qr_code(self, teacher_unique_id):
        """Delete QR code file for a teacher"""
        filepath = self.get_qr_code_path(teacher_unique_id)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

# Global instance
qr_generator = QRCodeGenerator() 