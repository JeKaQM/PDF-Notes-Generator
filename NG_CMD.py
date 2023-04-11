import PyPDF2
import openai
import requests
import os
import fitz
import time
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
from PyPDF2 import PdfReader

def read_pdf(file_path):
    doc = fitz.open(file_path)
    slide_texts = []

    for page in doc:
        slide_texts.append(page.get_text())

    return slide_texts

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"


def generate_notes(slide_texts, output_file, model='text-davinci-003', max_chunk_size=2048):
    # Initialize an empty string to store the generated notes
    notes = ""

    # Initialize a variable to store the total processing time
    total_processing_time = 0

    # Iterate through the slide_texts and generate notes for each slide
    for index, slide_text in enumerate(slide_texts):
        if len(slide_text.strip()) == 0:
            continue

        # Make sure the chunk size does not exceed the max_chunk_size
        chunk = slide_text[:max_chunk_size]

        prompt = f"Read the following slide content and create detailed notes with clear labels and important information:\nSlide {index + 1}:\n{chunk}"

        start_time = time.time()
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5,
        )
        end_time = time.time()

        # Calculate the time taken for processing the current slide
        processing_time = end_time - start_time
        total_processing_time += processing_time

        # Estimate the remaining time
        remaining_slides = len(slide_texts) - (index + 1)
        estimated_remaining_time = remaining_slides * (total_processing_time / (index + 1))

        # Append the generated notes to the notes string
        slide_notes = f"Slide {index + 1} Notes:\n{response.choices[0].text.strip()}\n\n"
        notes += slide_notes

        # Save the notes to the output file after each slide
        with open(output_file, 'a') as f:
            f.write(slide_notes)
            f.flush()

        # Print the progress and estimated time
        formatted_remaining_time = format_time(estimated_remaining_time)
        print(f"Processed slide {index + 1} of {len(slide_texts)}, estimated remaining time: {formatted_remaining_time}")

    return notes


def save_notes_to_file(notes, output_file):
    with open(output_file, 'w') as f:
        f.write(notes)

def main():
    # Get input and output file paths
    input_file = input("Enter the PDF file name (with .pdf extension): ")
    output_file_name = input("Enter the output file name (with .txt extension): ")
    output_file = f"notes/{output_file_name}"

    # Create the output directory if it doesn't exist
    if not os.path.exists("notes"):
        os.makedirs("notes")

    # Clear the output file if it exists
    if os.path.exists(output_file):
        open(output_file, 'w').close()

    # Read and extract text from PDF
    slide_texts = read_pdf(input_file)

    # Generate notes using OpenAI API
    notes = generate_notes(slide_texts, output_file)

    print("Notes generation completed!")


if __name__ == "__main__":
    main()
