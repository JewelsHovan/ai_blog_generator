#!/usr/bin/env python3
"""
Main script for running the Data Blog Generator
"""

import argparse
import os
from typing import List
from data_blog_generator import DataBlogGenerator
from pathlib import Path

AVAILABLE_MODELS = [
    "openai/gpt-4o-mini",
    "google/palm-2-chat-bison",
    "meta-llama/llama-2-70b-chat",
]

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Generate a data science blog post')
    parser.add_argument(
        '--context', '-c',
        type=str,
        help='Path to a text file containing the project context',
        required=True
    )
    
    # Create mutually exclusive group for images
    image_group = parser.add_mutually_exclusive_group(required=True)
    image_group.add_argument(
        '--images', '-i',
        nargs='+',
        help='Paths to individual visualization images'
    )
    image_group.add_argument(
        '--image-dir', '-d',
        type=str,
        help='Directory containing visualization images'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='blog_posts',
        help='Directory to save the generated blog post (default: blog_posts)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='OpenRouter API key (optional, can also use OPENAI_API_KEY environment variable)'
    )
    parser.add_argument(
        '--model',
        type=str,
        choices=AVAILABLE_MODELS,
        default="openai/gpt-4o-mini",
        help='Model to use for generation (default: openai/gpt-4o-mini)'
    )
    return parser.parse_args()

def read_context(context_path: str) -> str:
    """Read context from a file"""
    with open(context_path, 'r') as f:
        return f.read().strip()

def get_image_paths(args) -> List[str]:
    """Get list of image paths from either directory or individual files"""
    if args.images:
        return validate_images(args.images)
    else:
        return get_images_from_directory(args.image_dir)

def get_images_from_directory(directory: str) -> List[str]:
    """Get all image files from a directory"""
    image_paths = []
    dir_path = Path(directory)
    
    if not dir_path.is_dir():
        raise NotADirectoryError(f"Directory not found: {directory}")
    
    # Collect all image files
    for ext in IMAGE_EXTENSIONS:
        image_paths.extend(str(p) for p in dir_path.glob(f"*{ext}"))
    
    if not image_paths:
        raise ValueError(f"No image files found in directory: {directory}")
    
    # Sort for consistent ordering
    image_paths.sort()
    return validate_images(image_paths)

def validate_images(image_paths: List[str]) -> List[str]:
    """Validate image paths and return absolute paths"""
    valid_paths = []
    for path in image_paths:
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Image file not found: {path}")
        if not any(abs_path.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
            raise ValueError(f"Invalid image file type: {path}")
        valid_paths.append(abs_path)
    return valid_paths

def main():
    """Main function to run the blog post generator"""
    # Parse command line arguments
    args = parse_args()
    
    try:
        # Read and validate inputs
        context = read_context(args.context)
        image_paths = get_image_paths(args)
        
        print(f"\nFound {len(image_paths)} images:")
        for path in image_paths:
            print(f"  - {os.path.basename(path)}")
        
        # Initialize generator
        generator = DataBlogGenerator(openai_api_key=args.api_key, model_name=args.model)
        
        # Generate narrative ideas
        narrative_ideas = generator.generate_narrative_ideas(context)
        print("\nPotential Narrative Approaches:")
        for i, idea in enumerate(narrative_ideas, 1):
            print(f"{i}. {idea}")
        
        # Get user choice for narrative
        while True:
            try:
                choice = int(input("\nChoose a narrative approach (enter number): "))
                if 1 <= choice <= len(narrative_ideas):
                    chosen_narrative = narrative_ideas[choice - 1]
                    break
                print(f"Please enter a number between 1 and {len(narrative_ideas)}")
            except ValueError:
                print("Please enter a valid number")
        
        print("\nGenerating blog post...")
        # Generate blog post
        blog_post = generator.generate_blog_post(context, image_paths, chosen_narrative)
        
        # Save blog post
        output_path = generator.save_blog_post(blog_post, args.output_dir)
        
        print(f"\nBlog post generated successfully!")
        print(f"Output path: {output_path}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
