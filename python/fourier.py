import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog


def preprocess_image(filename: str) -> np.ndarray:
    """Load image, remove long straight lines (grid/background), return cleaned grayscale."""
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    # Adaptive threshold for binarization
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Use morphology to reduce noise
    kernel = np.ones((3, 3), np.uint8)
    clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # Detect lines with Hough transform
    edges = cv2.Canny(clean, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=80, maxLineGap=5)

    # Mask out detected lines
    mask = np.ones_like(clean) * 255
    if lines is not None:
        for x1, y1, x2, y2 in lines[:, 0]:
            cv2.line(mask, (x1, y1), (x2, y2), 0, 3)

    result = cv2.bitwise_and(clean, mask)
    return result


def extract_contour_from_jpg(filename: str, scale: float = 1/100) -> np.ndarray:
    """Extract the largest contour from a preprocessed JPG image."""
    preprocessed = preprocess_image(filename)
    edges = cv2.Canny(preprocessed, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = max(contours, key=cv2.contourArea)
    points = np.array([x[0] for x in cnt], dtype=np.float32)
    points = (points - points.mean(axis=0)) * scale
    return points[:, 0] + 1j * (-points[:, 1])  # complex plane


def fourier_transform(points: np.ndarray, n_terms: int = 1000):
    """Compute DFT of contour points."""
    N = len(points)
    freqs = np.fft.fftfreq(N)
    coefs = np.fft.fft(points) / N
    return freqs, coefs


def reconstruct_path(freqs, coefs, N=500, n_terms=1000):
    """Reconstruct curve from Fourier coefficients."""
    t = np.linspace(0, 1, N)
    path = np.zeros(N, dtype=complex)
    indices = np.argsort(np.abs(coefs))[-n_terms:]  # strongest terms
    for k in indices:
        path += coefs[k] * np.exp(2j * np.pi * freqs[k] * t * len(coefs))
    return path


def plot_and_save(path: np.ndarray, outfile: str = "fourier_output.png"):
    """Save and display Fourier reconstruction."""
    plt.figure(figsize=(6, 6))
    plt.plot(path.real, path.imag, color="blue")
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.savefig(outfile, bbox_inches="tight", dpi=150)
    plt.show()


def choose_file_gui() -> str:
    """Open file dialog to pick an image."""
    root = Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
    )
    root.destroy()
    return filepath


def main():
    parser = argparse.ArgumentParser(description="JPG → Fourier contour visualization")
    parser.add_argument("image", nargs="?", help="Path to image (JPG/PNG)")
    parser.add_argument("--terms", type=int, default=20000, help="Number of Fourier terms")
    parser.add_argument("--output", default="fourier_output.png", help="Output image filename")
    args = parser.parse_args()

    # If no image path given, open GUI
    image_path = args.image or choose_file_gui()
    if not image_path:
        print("No file selected. Exiting.")
        return

    points = extract_contour_from_jpg(image_path)
    freqs, coefs = fourier_transform(points)
    path = reconstruct_path(freqs, coefs, n_terms=args.terms)
    plot_and_save(path, args.output)


if __name__ == "__main__":
    main()
