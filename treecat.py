#!/usr/bin/env python3
import os

def tree_and_cat(root_dir="."):
    output = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        output.append(f"\n{dirpath}/")
        for filename in filenames:
            if filename == ".DS_Store":
                continue  # Skip .DS_Store files
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root_dir)
            output.append(f"\n-- {relative_path} --")
            output.append("\n```")
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    output.append(file.read())
            except Exception as e:
                output.append(f"Could not read file {relative_path}: {e}")
            output.append("\n```")
    return "\n".join(output)

def split_output(output, max_words=4000):
    words = output.split()
    chunks = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

if __name__ == "__main__":
    output = tree_and_cat()
    chunks = split_output(output)
    for index, chunk in enumerate(chunks):
        print(f"\n--- Copying chunk {index + 1}/{len(chunks)} to clipboard ---")
        chunk_safe = chunk.replace("'", "'\"'\"'")
        os.system(f"echo '{chunk_safe}' | pbcopy")
        input("Press Enter to copy the next chunk to the clipboard...")
