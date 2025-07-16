import qrcode
import qrcode.image.svg
import numpy as np
import os

def generate_qr_codes(urls, output_directory="tirpstansios_ribos_qr"):
    """
    Generates QR codes for a list of URLs and saves them to the specified directory.

    Parameters:
        urls (list of str): List of URLs to generate QR codes for.
        output_directory (str): Directory to save the QR code images.

    Returns:
        None
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for i, url in enumerate(urls):
        # Generate QR code
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
            image_factory=qrcode.image.svg.SvgFillImage,
        )
        #factory = qrcode.image.svg.SvgPathImage
        qr.add_data(url)
        qr.make(fit=True)
        print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
        # Create an image of the QR code
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image
        filename = os.path.join(output_directory, f"youtube_qrcode_{i + 1}.svg")
        #filename = os.path.join(output_directory, f"qrcode_{url.replace("https:","").replace("/","")}.svg")
        #filename = filename.replace("/","")
        img.save(filename)
        print(f"Saved QR code for {url} as {filename}")

if __name__ == "__main__":
    # Example array of URLs
    urls = [
        "https://www.youtube.com/watch?v=oWW71TRtUDE",
        "https://www.youtube.com/watch?v=xWJk63tjBJA",
        "https://www.youtube.com/watch?v=X6RN4GmJc0A",
        "https://www.youtube.com/watch?v=hVyn94TyaHE",
        "https://www.youtube.com/watch?v=eWyMu0NNx-U",
        "https://www.youtube.com/watch?v=VFXgkgpMAEA",
        "https://www.youtube.com/watch?v=4OEbJaeiATM",
        "https://www.youtube.com/watch?v=4XshGeu3P-Q",
        "https://www.youtube.com/watch?v=B7vndam0QEE",
    ]

    # Generate QR codes for the URLs
    generate_qr_codes(urls)
