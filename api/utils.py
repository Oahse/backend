from django.core.mail import EmailMessage
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import hashlib
import io
import os
import base64
from io import BytesIO
from PIL import Image
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class Util:
    @staticmethod
    def send_email(request, user, email, token, websitetype, type, subject,new_password=None):
        """
        Sends an email to the user for various purposes like password reset or email verification.

        Args:
            request: HTTP request object.
            user: User instance.
            email: Email address of the recipient.
            token: Token for email verification or password reset.
            websitetype: Type of website sending the email.
            type: Type of email (password_reset or email_verification).
            subject: Subject of the email.
        """
        current_site = get_current_site(request).domain
        uidb64 = urlsafe_base64_encode(user.pk.bytes)

        # Generate absolute URL based on the type of email
        if type == 'password_reset':
            current_site = get_current_site(request)
            absurl = f'http://{current_site.domain}/#/reset-password/{uidb64}/{token}?new_password={new_password}'
            email_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Password Reset</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; }}
                    .container {{ max-width: 600px; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
                    .header {{ text-align: center; padding: 10px 0; border-bottom: 1px solid #ddd; }}
                    .header h1 {{ margin: 0; color: #4CAF50; }}
                    .content {{ padding: 20px; }}
                    .content p {{ margin: 10px 0; line-height: 1.6; }}
                    .reset-button {{ display: block; width: 200px; margin: 20px auto; padding: 10px 0; text-align: center; background-color: #4CAF50; color: #fff; text-decoration: none; border-radius: 5px; font-size: 16px; }}
                    .footer {{ text-align: center; padding: 10px 0; border-top: 1px solid #ddd; margin-top: 20px; color: #888; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Password Reset</h1>
                    </div>
                    <div class="content">
                        <p>Hi {user.first_name},</p>
                        <p>Click the button below to reset your password:</p>
                        <a href="{absurl}" class="reset-button">Reset Password</a>

                        <p>or click on the link below</p>
                        <a>{absurl}</a>
                        <p>If you did not request this email, please ignore it.</p>
                    </div>
                    <div class="footer">
                        <p>Thank you for using our service!</p>
                    </div>
                </div>
            </body>
            </html>
            """
        elif type == 'email_verification':
            current_site = get_current_site(request)
            absurl = f'http://{current_site.domain}/#/verify-email/{uidb64}/{token}/'
            email_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Email Verification</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; }}
                    .container {{ max-width: 600px; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
                    .header {{ text-align: center; padding: 10px 0; border-bottom: 1px solid #ddd; }}
                    .header h1 {{ margin: 0; color: #4CAF50; }}
                    .content {{ padding: 20px; }}
                    .content p {{ margin: 10px 0; line-height: 1.6; }}
                    .verify-button {{ display: block; width: 200px; margin: 20px auto; padding: 10px 0; text-align: center; background-color: #4CAF50; color: #fff; text-decoration: none; border-radius: 5px; font-size: 16px; }}
                    .footer {{ text-align: center; padding: 10px 0; border-top: 1px solid #ddd; margin-top: 20px; color: #888; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Email Verification</h1>
                    </div>
                    <div class="content">
                        <p>Hi {user.first_name},</p>
                        <p>Click the link below to verify your email address:</p>
                        <a href="{absurl}" class="verify-button">Verify Email</a>
                        <p>or click on the link below</p>
                        <a>{absurl}</a>
                        <p>If you did not request this email, please ignore it.</p>
                    </div>
                    <div class="footer">
                        <p>Thank you for using our service!</p>
                    </div>
                </div>
            </body>
            </html>
            """
        else:
            current_site = get_current_site(request)
            absurl = f'http://{current_site.domain}/#/verify-email/{uidb64}/{token}/'
            email_body = f'Hi,\nUse link below to verify your email \n{absurl}'

        # Create and send email message
        try:
            email_subject = subject
            email_to = [email]
            email = EmailMessage(
                email_subject,
                email_body,
                websitetype,
                email_to,
            )
            email.send(fail_silently=False)
        except Exception as e:
            print(e)
            return False
        return True
    
    
    @staticmethod
    def hash_password(password, salt=None):
        if salt is None:
            salt = os.urandom(16)  # Generate a random salt
        
        # Encode the password and salt
        encoded_password = password.encode('utf-8')
        
        # Hash the combined bytes using SHA-256
        hashed = hashlib.sha256(encoded_password + salt).hexdigest()
        
        # Return the salt and hashed password as a string
        return f'{salt.hex()}${hashed}'

    @staticmethod
    def verify_password(stored_password, provided_password):
        # Split the stored password into salt and hashed password
        salt_hex, stored_hash = stored_password.split('$')
        
        # Decode the salt from hexadecimal to bytes
        salt = bytes.fromhex(salt_hex)
        
        # Hash the provided password with the same salt
        computed_hash = hashlib.sha256((provided_password.encode('utf-8') + salt)).hexdigest()
        
        # Compare the stored hash with the computed hash
        return stored_hash == computed_hash
    
    @staticmethod
    def gen_qrcode(data_to_encode, logo):

        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,  # Controls the size of the QR Code
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction
            box_size=10,  # Size of each box in the QR code
            border=4,  # Border size
        )

        # Add data to the instance
        qr.add_data(data_to_encode)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        qr_img = qr.make_image(fill='black', back_color='white').convert('RGB')

        # Load the logo image
        logo = Image.open(logo)

        # Calculate dimensions
        qr_width, qr_height = qr_img.size
        logo_width, logo_height = logo.size

        # Scale the logo to fit into the QR code
        logo_size = qr_width // 4
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        # Calculate logo position
        logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

        # Paste the logo image into the QR code image
        qr_img.paste(logo, logo_pos, logo)

        # # Save the final image
        # qr_img.save('qr_with_logo.png')

        # Save the final image to a bytes buffer
        buffered = BytesIO()
        qr_img.save(buffered, format="PNG")
        
        
        # Encode the image to base64
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return img_str

    def image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string

    def base64_to_image(base64_string, output_path):
        image_data = base64.b64decode(base64_string)
        with open(output_path, "wb") as image_file:
            image_file.write(image_data)
    
    def pdf_to_base64(pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read()).decode('utf-8')
        return encoded_string
    
    def base64_to_pdf(base64_string, output_path):
        with open(output_path, "wb") as pdf_file:
            pdf_file.write(base64.b64decode(base64_string))

    @staticmethod
    def generate_pdf_receipt_in_memory(order_data, logo_path):
        buffer = io.BytesIO()
        
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        logo = Image.open(logo_path)
        logo_width, logo_height = logo.size
        aspect = logo_height / float(logo_width)
        logo_width = 2 * inch
        logo_height = logo_width * aspect
        c.drawImage(logo_path, (width - logo_width) / 2, height - logo_height - 20, logo_width, logo_height)

        text = c.beginText(1 * inch, height - logo_height - 50)
        text.setFont("Helvetica", 12)
        text.setFillColor(colors.black)

        text.textLine(f"Order ID: {order_data['order_id']}")
        text.textLine(f"Date: {order_data['date']}")
        text.textLine(f"Customer: {order_data['customer_name']}")
        text.textLine(f"Address: {order_data['customer_address']}")
        text.textLine("")
        text.textLine("Items:")
        
        for item in order_data['items']:
            text.textLine(f"- {item['name']} (x{item['quantity']}): ${item['price']:.2f}")
        
        text.textLine("")
        text.textLine(f"Total: ${order_data['total']:.2f}")

        c.drawText(text)
        c.save()

        # Get the PDF binary data
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()

        # Convert PDF binary data to base64
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        return pdf_base64
    

# Example usage
# order_data = {
#     "order_id": "123456",
#     "date": "2024-06-19",
#     "customer_name": "John Doe",
#     "customer_address": "123 Elm Street, Springfield",
#     "items": [
#         {"name": "Widget A", "quantity": 2, "price": 19.99},
#         {"name": "Widget B", "quantity": 1, "price": 29.99},
#         {"name": "Widget C", "quantity": 3, "price": 9.99},
#     ],
#     "total": 99.94
# }

# pdf_base64 = Util.generate_pdf_receipt_in_memory(order_data, "oahse_logo.png")
# print(pdf_base64)


# # Example usage:
# data = "https://www.example.com"
# logo_path = "oahse_logo.png"

# # Generate QR code with logo and convert to base64
# qr_code_base64 = Util.gen_qrcode(data, logo_path)
# print("QR Code Base64:", qr_code_base64)

# # Convert base64 back to image
# output_path = "qr_with_logo.png"
# Util.base64_to_image(qr_code_base64, output_path)
# print("Image saved to:", output_path)
    