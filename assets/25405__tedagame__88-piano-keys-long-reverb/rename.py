import os
import re

def rename_piano_files(folder_path):
    # This pattern matches both: c5, f#4, and f4#
    pattern = re.compile(r'_([a-gA-G])(#?)(\d)#?\.ogg$|_([a-gA-G])(\d)#\.ogg$')

    for filename in os.listdir(folder_path):
        if filename.endswith('.ogg'):
            match = pattern.search(filename)

            if match:
                # Normalize sharp notation
                if match.group(1):  # e.g., group(1)=f, group(2)=#, group(3)=4
                    note = f"{match.group(1).lower()}{match.group(2)}{match.group(3)}"
                else:  # handle the 'f4#' case as group(4)=f, group(5)=4
                    note = f"{match.group(4).lower()}#{match.group(5)}"

                new_filename = f"{note}.ogg"
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_filename)

                # Check before renaming
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"✅ Renamed: {filename} → {new_filename}")
                else:
                    print(f"⚠️ Skipped (already exists): {new_filename}")
            else:
                print(f"❌ Skipped (no match): {filename}")

# Run for current folder
pathh = os.path.dirname(os.path.abspath(__file__))
rename_piano_files(pathh)
