from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import os
import random
import string
import hashlib
import time
import shutil
import math
import concurrent.futures


# Resize the image
def resize_image(img):
    # Randomly resize the image by a small percentage
    resize_factor = random.uniform(0.9, 1.5)
    # height_resize_factor = random.uniform(0.9, 1.5)
    new_width = int(img.width * resize_factor)
    new_height = int(img.height * resize_factor)

    exif = getattr(img, '_getexif', lambda: None)()
    resized_img = img.resize((new_width, new_height), Image.BICUBIC)
    return resized_img

# Function to add random noise to an image
def add_noise(image):
    # Define range for random transformations
    # rotation_range = (-5, 5)  # Rotate image by -5 to 5 degrees
    blur_radius_range = (0, 1)  # Apply Gaussian blur with radius 0 to 1
    brightness_factor_range = (0.8, 1.2)  # Adjust brightness by 20%

    # Apply random rotation
    # rotation_angle = random.uniform(*rotation_range)
    # rotated_image = image.rotate(rotation_angle)

    # Apply random blur
    blur_radius = random.uniform(*blur_radius_range)
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # Apply random brightness adjustment
    brightness_factor = random.uniform(*brightness_factor_range)
    final_image = ImageEnhance.Brightness(blurred_image).enhance(brightness_factor)

    return final_image

# Function to generate a random string of alphanumeric characters
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to compute the hash of an image
def compute_image_hash(image):
    hash_md5 = hashlib.md5()
    with open(image, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def images_processor(args):
    input_dir, images_dir, filename, output_dir = args
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        # Open image
        input_path = os.path.join(input_dir, images_dir, filename)
        image = Image.open(input_path)
        fixed_image = ImageOps.exif_transpose(image)

        # Add random noise to image
        # noisy_image = add_noise(image)
        resized_image = resize_image(fixed_image)
        noisy_image = add_noise(resized_image)

        image_name = filename.split('.')[0]

        # Generate random filename
        random_filename = image_name + '_' + generate_random_string(5) + '.jpg'

        # Save processed image
        try:
            os.makedirs(os.path.join(output_dir, images_dir))
        except:
            pass
        output_path = os.path.join(output_dir, images_dir, random_filename)
        noisy_image.save(output_path)
        noisy_image.close()

        print(f"Processed: {filename} -> {random_filename}", end=' ')

        # Compute hash of original and processed images
        original_hash = compute_image_hash(input_path)
        processed_hash = compute_image_hash(output_path)

        # Check if hashes are the same
        if original_hash == processed_hash:
            print("Hashes match!")
        else:
            print("Hashes do not match!")

# Function to process images in a directory
def run(input_dir, output_dir):
    # Ensure output directory exists and is empty
    try:
        shutil.rmtree(output_dir)
    except:
        pass
    os.makedirs(output_dir, exist_ok=True)

    # Create a list of tuples containing arguments for images_processor
    arguments_list = []
    for images_dir in os.listdir(input_dir):
        image_files = os.listdir(os.path.join(input_dir, images_dir))
        for filename in image_files:
            arguments_list.append((input_dir, images_dir, filename, output_dir))

    # Process images using multiprocessing
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # result = list(executor.map(images_processor, arguments_list))
        executor.map(images_processor, arguments_list)


# Example usage
if __name__ == "__main__":
    input_directory = "../Listings_Pictures/originals"
    output_directory = "../Listings_Pictures/mods"

    start_time = time.perf_counter()
    run(input_directory, output_directory)
    end_time = time.perf_counter()

    running_time = end_time - start_time
    minutes = math.floor(running_time // 60)
    seconds = math.ceil((running_time % 1) * 60)
    mins = "mins" if minutes > 1 else "min"
    secs = "secs" if seconds > 1 else "sec"

    print(f"Running time: {minutes}{mins} {seconds}{secs}")
    # print("result: ", result)