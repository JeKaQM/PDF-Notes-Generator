import os
import openai
import PyPDF2 as pdf
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

stop_generation = False


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

def read_pdf(input_file):
    pdfFileObj = open(input_file, 'rb')
    pdfReader = pdf.PdfReader(pdfFileObj)
    num_pages = len(pdfReader.pages)
    slide_texts = [pdfReader.pages[i].extract_text() for i in range(num_pages)]
    pdfFileObj.close()
    return slide_texts

def generate_notes(slide_texts, output_file, user_prompt, model='text-davinci-003', max_chunk_size=2048):
    global stop_generation
    notes = ""
    total_processing_time = 0
    progress_var.set(f"Processing slide 0 of {len(slide_texts)}")

    progress_bar['maximum'] = len(slide_texts)
    progress_bar['value'] = 0
    for index, slide_text in enumerate(slide_texts):
        if stop_generation:
            break

        chunk = slide_text[:max_chunk_size]

        prompt = f"{user_prompt}\nSlide {index + 1}:\n{chunk}"

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

        processing_time = end_time - start_time
        total_processing_time += processing_time

        remaining_slides = len(slide_texts) - (index + 1)
        estimated_remaining_time = remaining_slides * (total_processing_time / (index + 1))

        slide_notes = f"Slide {index + 1} Notes:\n{response.choices[0].text.strip()}\n\n"
        notes += slide_notes

        with open(output_file, 'a', encoding='UTF-8') as f:
            f.write(slide_notes)
            f.flush()

        formatted_remaining_time = format_time(estimated_remaining_time)
        progress_var.set(f"Processing slide {index + 1} of {len(slide_texts)}")
        time_var.set(f"Estimated Remaining Time: {formatted_remaining_time}")
        progress_bar['value'] += 1
        root.update()

        
    progress_var.set("Notes generation completed.")
    return notes
def stop_notes_generation():
    global stop_generation
    stop_generation = True
    progress_var.set("Stopping notes generation...")
def browse_input_file():
    global input_file
    input_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    input_var.set(f"Selected file: {input_file}")

def browse_output_file():
    global output_file
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    output_var.set(f"Selected file: {output_file}")

def main():
    if not os.path.exists("notes"):
        os.makedirs("notes")

    user_prompt = prompt_entry.get()
    slide_texts = read_pdf(input_file)
    generate_notes(slide_texts, output_file, user_prompt)
    progress_var.set("Notes generation completed!")

root = tk.Tk()
root.title("AI Notes Generator")

input_var = tk.StringVar()
output_var = tk.StringVar()
progress_var = tk.StringVar()

input_button = tk.Button(root, text="Select input PDF", command=browse_input_file)
input_button.pack(pady=10)
input_label = tk.Label(root, textvariable=input_var)
input_label.pack()

output_button = tk.Button(root, text="Select output file", command=browse_output_file)
output_button.pack(pady=10)
output_label = tk.Label(root, textvariable=output_var)
output_label.pack()
prompt_label = tk.Label(root, text="Enter your custom prompt:")
prompt_label.pack(pady=10)
prompt_entry = tk.Entry(root, width=50)
prompt_entry.pack(pady=10)

generate_button = tk.Button(root, text="Generate Notes", command=main)
generate_button.pack(pady=10)

progress_label = tk.Label(root, textvariable=progress_var)
progress_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(pady=10)

time_var = tk.StringVar()
time_label = tk.Label(root, textvariable=time_var)
time_label.pack(pady=10)

stop_button = tk.Button(root, text="Stop Generation", command=stop_notes_generation)
stop_button.pack(pady=10)

root.mainloop()


###Example of good prompt
#Generate notes for each slide,provide short context to the slide, focusing on definitions, key values and ignoring any empty slides or the ones that do not provide any useful information.Only do bullet points.
