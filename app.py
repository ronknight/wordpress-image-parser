import os
import re

def delete_wordpress_resized_images(folder_path, recursive=False):
    # Regex pattern to identify WordPress resized images
    wp_resize_pattern = re.compile(r"(.+)-\d+x\d+(\.\w+)$")

    deleted_files = []
    skipped_files = []

    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        # Only check subdirectories if recursive option is enabled
        if not recursive and root != folder_path:
            continue
        
        # Dictionary to track original images (without the WP resize suffix)
        originals = {file for file in files if not wp_resize_pattern.search(file)}
        
        # Identify and delete WordPress resized images
        for file in files:
            match = wp_resize_pattern.match(file)
            if match:
                original_filename = match.group(1) + match.group(2)  # Original image name
                if original_filename in originals:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    deleted_files.append(file_path)
                else:
                    skipped_files.append(file)  # Track files where originals are missing
        
        if not recursive:
            break

    return deleted_files, skipped_files

# Specify the folder path
folder_path = "/path/to/your/image/folder"
recursive = True  # Set to True to parse subfolders

# Run the cleanup function
deleted_files, skipped_files = delete_wordpress_resized_images(folder_path, recursive)

print("Deleted files:")
for file in deleted_files:
    print(file)

print("\nSkipped files (originals missing):")
for file in skipped_files:
    print(file)
