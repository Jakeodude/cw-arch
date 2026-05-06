import zipfile
import os

output_file = 'content_warning.apworld'

# A list of folders and files we NEVER want inside the apworld
ignore_list = [
    '.git', 
    '.vscode', 
    '__pycache__', 
    'build_apworld.py', 
    '.gitignore',
    '.gitattributes', # Added this!
    'CLAUDE.md',      # Added this!
    'README.md'       # Optional: Remove this if you want the readmes included!
]

print("Packing APWorld...")

# Open a new zip file
with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('.'):
        
        # Tell os.walk to completely skip our ignored folders
        dirs[:] = [d for d in dirs if d not in ignore_list]
        
        for file in files:
            # Skip ignored files and any existing .apworld / .zip files
            if file in ignore_list or file.endswith('.apworld') or file.endswith('.zip'):
                continue
                
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, '.')
            
            # Add the file to the zip
            zipf.write(file_path, arcname)
            print(f"Added: {arcname}")

print(f"\nSuccessfully built clean {output_file}!")