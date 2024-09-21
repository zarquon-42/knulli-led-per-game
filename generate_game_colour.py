#!/usr/bin/env python3

import sys
import os
import argparse
from PIL import Image, UnidentifiedImageError
import numpy as np
from collections import Counter
import re

def is_ignored_color(color, black_threshold=30, white_threshold=225):
    """
    Returns True if the color is close to black or white.
    """
    if all(c < black_threshold for c in color):  # Check for black
        return True
    if all(c > white_threshold for c in color):  # Check for white
        return True
    return False

def rgb_to_hex(color):
    """
    Convert an RGB color tuple to a hex string.
    """
    return "#{:02X}{:02X}{:02X}".format(color[0], color[1], color[2])

def rgb_to_hsv(color):
    """
    Convert an RGB color tuple to an HSV color tuple.
    """
    color = np.array(color) / 255.0
    max_val = np.max(color)
    min_val = np.min(color)
    delta = max_val - min_val
    v = max_val
    s = delta / max_val if max_val != 0 else 0

    if delta == 0:
        h = 0
    else:
        if color[0] == max_val:
            h = (color[1] - color[2]) / delta
        elif color[1] == max_val:
            h = (color[2] - color[0]) / delta + 2
        else:
            h = (color[0] - color[1]) / delta + 4
        h /= 6.0
        if h < 0:
            h += 1
    
    h = int(h * 360)
    s = int(s * 100)
    v = int(v * 100)
    
    return (h, s, v)

def hsv_to_rgb(hsv):
    """
    Convert an HSV color tuple to an RGB color tuple.
    """
    h, s, v = hsv
    s /= 100.0
    v /= 100.0
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

def adjust_brightness(color):
    """
    Adjust the color so that its saturation and value are at least 80%.
    """
    hsv = rgb_to_hsv(color)
    h, s, v = hsv
    if s < 80:
        s = 80
    if v < 80:
        v = 80
    adjusted_color = hsv_to_rgb((h, s, v))
    return adjusted_color

def get_dominant_color(image_path, num_colors=1, output_format='rgb', brighten=False, debug=False):
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Resize image to reduce computation time (optional)
        image = image.resize((100, 100))
        
        # Convert image to RGB if it is in a different mode
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Convert the image to a numpy array
        pixels = np.array(image)
        
        # Reshape the image to be a list of pixels
        pixels = pixels.reshape(-1, 3)
        
        # Filter out black and white pixels
        filtered_pixels = [tuple(pixel) for pixel in pixels if not is_ignored_color(pixel)]
        
        # Count the frequency of each pixel
        pixel_counts = Counter(filtered_pixels)
        
        # Get the most common colors
        most_common_colors = pixel_counts.most_common(num_colors)
        
        # Print progress message if needed
        if debug:
            print(f"Processed file: {image_path}")
        
        # Adjust color if needed
        if brighten:
            most_common_colors = [(adjust_brightness(color), count) for color, count in most_common_colors]

        # Return the dominant color(s)
        return most_common_colors

    except UnidentifiedImageError:
        if debug:
            sys.stderr.write(f"Error: Unable to open image file '{image_path}'. The file is not a valid image.\n")
        return None

    except Exception as e:
        if debug:
            sys.stderr.write(f"An unexpected error occurred with '{image_path}': {e}\n")
        return None

def mean_color(colors):
    """
    Calculate the mean RGB color from a list of RGB tuples.
    """
    if not colors:
        return None

    # Convert list of RGB values to numpy array for easy manipulation
    colors_array = np.array(colors)
    
    # Calculate mean across each RGB channel
    mean_rgb = np.mean(colors_array, axis=0)
    
    # Convert the result to integers (since RGB values must be integers)
    return tuple(map(int, mean_rgb))

def brightness(color):
    """
    Calculate the brightness of an RGB color using the formula:
    brightness = 0.299*R + 0.587*G + 0.114*B
    This is a standard formula for determining perceived brightness.
    """
    return 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]

def brightest_color(colors):
    """
    Find the brightest color from a list of RGB tuples.
    """
    if not colors:
        return None

    # Sort colors by their brightness, descending
    return max(colors, key=brightness)

def print_progress(message, output_format, debug=False):
    """
    Print progress messages based on the output format.
    """
    if debug:
        print(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Determine the dominant color of image files.")
    parser.add_argument('path_to_images', type=str, help="Path to the directory containing image files.")
    parser.add_argument('rom_name', type=str, help="ROM name to match image files.")
    parser.add_argument('--brightest', action='store_true', help="Use the brightest color.")
    parser.add_argument('--mean', action='store_true', help="Use the mean color.")
    parser.add_argument('--brighten', action='store_true', help="Adjust the color to ensure S and V are at least 80%.")
    parser.add_argument('--rgb', action='store_true', help="Display color in RGB format.")
    parser.add_argument('--hex', action='store_true', help="Display color in Hex format.")
    parser.add_argument('--hsv', action='store_true', help="Display color in HSV format.")
    parser.add_argument('-d', '--debug', action='store_true', help="Display debug information.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Display verbose information.")

    args = parser.parse_args()

    # Determine display mode
    if args.brightest and args.mean:
        sys.stderr.write("Error: Choose either --brightest or --mean, not both.\n")
        sys.exit(1)
    display_mode = 'brightest' if args.brightest else 'mean' if args.mean else 'brightest'

    # Determine output format
    if args.rgb:
        output_format = 'rgb'
    elif args.hex:
        output_format = 'hex'
    elif args.hsv:
        output_format = 'hsv'
    elif args.verbose:
        output_format = 'verbose'
    else:
        output_format = 'rgb'

    # Check if the directory exists
    if not os.path.exists(args.path_to_images):
        sys.stderr.write(f"Error: The directory '{args.path_to_images}' does not exist.\n")
        sys.exit(1)

    if not os.path.isdir(args.path_to_images):
        sys.stderr.write(f"Error: '{args.path_to_images}' is not a valid directory.\n")
        sys.exit(1)

    # Regex to match files with rom_name followed by a dash and a description
    rom_pattern = re.compile(rf"^{args.rom_name}-\w+\.(jpg|png)$")

    # List to store the dominant colors of all matching files
    all_dominant_colors = []

    # Loop over all files in the directory
    for file_name in os.listdir(args.path_to_images):
        if rom_pattern.match(file_name):
            # Full path to the image
            image_path = os.path.join(args.path_to_images, file_name)
            print_progress(f"Processing file: {image_path}", output_format, args.debug)
            
            # Get the dominant color of the image
            dominant_color = get_dominant_color(image_path, output_format=output_format, brighten=args.brighten, debug=args.debug)
           
            if dominant_color:
                rgb_color = dominant_color[0][0]  # Extract the RGB value of the most common color
                all_dominant_colors.append(rgb_color)

    # Check if any colors were collected
    if not all_dominant_colors:
        sys.stderr.write(f"No matching images found for ROM name '{args.rom_name}'.\n")
        sys.exit(1)

    # Calculate the mean color or find the brightest color based on user input
    if display_mode == "mean":
        result_color = mean_color(all_dominant_colors)
    elif display_mode == "brightest":
        result_color = brightest_color(all_dominant_colors)

    if result_color:
        result_hex_color = rgb_to_hex(result_color)
        result_hsv_color = rgb_to_hsv(result_color)
        
        # Adjust brightness if needed
        if args.brighten:
            original_color = result_color
            result_color = adjust_brightness(result_color)
            result_hex_color = rgb_to_hex(result_color)
            result_hsv_color = rgb_to_hsv(result_color)
            
        # Display output based on the selected output format
        if output_format == "rgb":
            print(f"{result_color[0]} {result_color[1]} {result_color[2]}")
        elif output_format == "hex":
            print(f"{result_hex_color[1:]}")
        elif output_format == "hsv":
            print(f"{result_hsv_color[0]} {result_hsv_color[1]} {result_hsv_color[2]}")
        elif output_format == "verbose":
            if args.brighten:
                print(f"The \"Brightened\" {display_mode} color across all images is: {result_color} (RGB) / {result_hex_color} (Hex) / {result_hsv_color} (HSV)")
                print(f"Original color (RGB): {original_color} / (Hex): {rgb_to_hex(original_color)} / (HSV): {rgb_to_hsv(original_color)}")
            else:
                print(f"The {display_mode} color across all images is: {result_color} (RGB) / {result_hex_color} (Hex) / {result_hsv_color} (HSV)")
    else:
        sys.stderr.write(f"Error: Unable to calculate the {display_mode} color.\n")
