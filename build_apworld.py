import zipfile
import os

output_file = 'content_warning.apworld'
world_folder_name = 'content_warning'  # The single directory Archipelago expects!

# A list of folders and files we NEVER want inside the apworld
ignore_list = [
    '.git',
    '.vscode',
    '__pycache__',
    'build_apworld.py',
    '.gitignore',
    '.gitattributes',
    'CLAUDE.md',
    'devnotes'
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
            
            # THE MAGIC FIX: Prepend the world folder name to the zip path!
            relative_path = os.path.relpath(file_path, '.')
            arcname = os.path.join(world_folder_name, relative_path)

            # Add the file to the zip
            zipf.write(file_path, arcname)
            print(f"Added: {arcname}")

print(f"\nSuccessfully built clean {output_file}!")