import hashlib
import sys
import os

def calculate_file_hash(filename, algorithm='sha256'):
    """
    Calculates the hash of a file using a specified algorithm.
    Reads the file in chunks to handle large files efficiently.
    """
    if algorithm == 'sha256':
        h = hashlib.sha256()
    elif algorithm == 'md5':
        h = hashlib.md5()
    else:
        return f"Error: Unsupported algorithm {algorithm}"
        
    try:
        with open(filename, 'rb') as file:
            # Read and update hash string chunk by chunk
            while chunk := file.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        return f"Error: File not found at '{filename}'"
    except IOError as e:
        return f"Error reading file: {e}"

if __name__ == "__main__":
    # Check if exactly one argument (the file path) was provided
    if len(sys.argv) != 2:
        print("Usage: tiny hash <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Check if the file actually exists before trying to hash it
    if not os.path.isfile(file_path):
        print(f"Error: File not found at '{file_path}'")
        sys.exit(1)

    file_hash = calculate_file_hash(file_path, algorithm='sha256')
    
    if "Error" not in file_hash:
        print(f"File: {file_path}")
        print(f"SHA256 Hash: {file_hash}")
    else:
        print(file_hash)
        sys.exit(1)
