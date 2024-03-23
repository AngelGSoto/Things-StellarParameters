#!/bin/bash

# Specify the input and output directories
input_directory="DeltaValues"
output_directory="DeltaValues_resize"

# Create the output directory if it doesn't exist
mkdir -p "$output_directory"

# Loop through each PNG file in the input directory
for file in "$input_directory"/*.png; do
    # Extract the file name without the path and extension
    filename=$(basename -- "$file")
    filename_noext="${filename%.*}"

    # Construct the output file path
    output_file="$output_directory/${filename_noext}_resized.png"

    # Resize the image using ImageMagick's convert command
    convert "$file" -resize 50% "$output_file"
done
