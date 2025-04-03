Text Image Converter for People with Slow Internet


A lightweight Python application to convert images into compact text representations and back.

This project is designed to help users with slow internet connections or limited device resources efficiently share and view simple images.
By converting images into a compact text format, the program minimizes data usage while preserving the essential visual information.
It also allows decoding the text back into an image, making it a versatile tool for creative and practical use cases.

Features
Image-to-Text Conversion :
Convert black-and-white or grayscale images (up to 100x100 pixels) into a compact text representation.
Each pixel is encoded as a single digit (0–9), where 0 represents black and 9 represents white.
The resulting text is easy to copy, share, and store.
Text-to-Image Decoding :
Decode the text representation back into an image.
Supports real-time visualization of decoded images within the application.
Compact and Lightweight :
Optimized for minimal data usage, making it ideal for environments with limited bandwidth or storage.
User-Friendly Interface :
Built with PySide6 , the application features a clean and intuitive GUI with a dark theme and light-gray buttons.
Centered image previews ensure a balanced layout.
Cross-Platform Compatibility :
Works on Windows, macOS, and Linux.
Use Cases
Low-Bandwidth Environments :
Share simple images (e.g., icons, logos, or small graphics) without consuming excessive bandwidth.
Creative Projects :
Experiment with text-based image encoding for retro-style designs, ASCII art, or educational purposes.
Resource-Constrained Devices :
Use the program on older devices or systems with limited processing power.
Learning Tool :
Explore how images can be represented as text and understand the basics of image processing.
How It Works
Load an Image :
Upload a black-and-white or grayscale image (up to 100x100 pixels). Larger images are automatically resized.
Convert to Text :
Generate a compact text representation of the image. Each pixel is encoded as a single digit (0–9).
Copy the Text :
Copy the generated text to your clipboard for sharing or storage.
Decode Text Back to Image :
Paste the text into the input field and decode it back into an image.
Save the Image :
Save the decoded image to your computer in PNG or JPEG format.
Built With
PySide6 : For the graphical user interface.
Pillow : For image loading, processing, and saving.
NumPy : For efficient array manipulation.
