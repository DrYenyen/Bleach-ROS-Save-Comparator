import tkinter as tk
from tkinter import scrolledtext, filedialog

def read_save_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def compare_saves():
    save_files = filedialog.askopenfilenames(title="Select Save Files", filetypes=[("Save Files", "*")])
    if len(save_files) < 2:
        output_text.insert(tk.END, "Please select at least two save files.\n")
        return

    save_data = [read_save_file(file) for file in save_files]
    min_length = min(len(data) for data in save_data)
    base_offset = 0x00000000 

    differences = []
    for offset in range(min_length):
        values = [data[offset] for data in save_data]
        if len(set(values)) > 1:  # If there's a difference
            line_start = offset & 0xFFFFFFF0  # Align to the start of the line like in HxD cuz me dummy
            location = offset + base_offset
            context_range = range(max(0, line_start), min(min_length, line_start + 16))
            formatted_contexts = [" ".join([hex(byte)[2:].zfill(2).upper() for byte in data[context_range.start:context_range.stop]]) for data in save_data]
            differences.append((line_start, location, formatted_contexts))

    output_text.delete('1.0', tk.END)
    for offset, location, contexts in differences:
        output_text.insert(tk.END, f"Offset: {offset:08X}\nLocation: {location:08X}\n") # Offset is the start of the line Location is the Space in the line that has a different value
        for i, context in enumerate(contexts):
            output_text.insert(tk.END, f"File {i+1} Context: {context}\n")
        output_text.insert(tk.END, "-" * 50 + "\n")

def clear_output():
    output_text.delete('1.0', tk.END) 

# Builds the GUI window 
root = tk.Tk()
root.title("Ez Bleach Save Comparator")
root.geometry("1000x700")

frame = tk.Frame(root)
frame.pack(pady=10)

# Select button can choose multiple files
compare_button = tk.Button(frame, text="Select & Compare Saves", command=compare_saves)
compare_button.pack(side=tk.LEFT, padx=10)

# Clear current output
clear_button = tk.Button(frame, text="Clear Output", command=clear_output)
clear_button.pack(side=tk.LEFT, padx=10)

# Output window
output_text = scrolledtext.ScrolledText(root, width=120, height=35)
output_text.pack(padx=10, pady=10)

root.mainloop()