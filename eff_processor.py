import os
import hashlib
import base64
import zipfile
import shutil
import argparse

def calculate_md5_base64(filepath):
    """Calculate the MD5 hash of a file and return it in Base64 format."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    md5_hash = hasher.digest()
    return base64.b64encode(md5_hash).decode('utf-8')

def process_eff_package(eff_file_path, output_folder):
    """Process the EFF package to recalculate hashes and repackage."""
    if not zipfile.is_zipfile(eff_file_path):
        raise ValueError(f"{eff_file_path} is not a valid zip file.")
    
    # Step 1: Unzip the .eff file
    with zipfile.ZipFile(eff_file_path, 'r') as eff_zip:
        eff_zip.extractall(output_folder)
    
    lst_file_path = os.path.join(output_folder, 'eff.lst')
    dat_file_path = os.path.join(output_folder, 'eff.dat')
    
    if not os.path.exists(lst_file_path) or not os.path.exists(dat_file_path):
        raise FileNotFoundError("eff.lst or eff.dat file is missing in the EFF package.")
    
    # Step 2: Unzip the .dat file to a subfolder
    dat_folder = os.path.join(output_folder, 'dat')
    os.makedirs(dat_folder, exist_ok=True)
    with zipfile.ZipFile(dat_file_path, 'r') as dat_zip:
        dat_zip.extractall(dat_folder)
    
    # Step 3: Recalculate MD5 Base64 hashes for files in the .dat folder
    file_hashes = {}
    for root, _, files in os.walk(dat_folder):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, dat_folder)
            file_hashes[relative_path] = calculate_md5_base64(file_path)
    
    # Step 4: Update the eff.lst file with new hashes
    with open(lst_file_path, 'r') as lst_file:
        lst_lines = lst_file.readlines()
    
    updated_lines = []
    for line in lst_lines:
        parts = line.strip().split()
        if len(parts) == 2 and parts[0] in file_hashes:
            updated_lines.append(f"{parts[0]} {file_hashes[parts[0]]}\n")
        else:
            updated_lines.append(line)
    
    with open(lst_file_path, 'w') as lst_file:
        lst_file.writelines(updated_lines)
    
    # Step 5: Repackage the .dat folder into a .dat file
    new_dat_file_path = os.path.join(output_folder, 'new_eff.dat')
    with zipfile.ZipFile(new_dat_file_path, 'w') as new_dat_zip:
        for root, _, files in os.walk(dat_folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, dat_folder)
                new_dat_zip.write(file_path, relative_path)
    
    # Step 6: Recalculate MD5 Base64 hash for the new .dat file
    new_dat_hash = calculate_md5_base64(new_dat_file_path)
    with open(lst_file_path, 'a') as lst_file:
        lst_file.write(f"eff.dat {new_dat_hash}\n")
    
    # Step 7: Repackage eff.lst and new_eff.dat into a new .eff file
    new_eff_file_path = os.path.join(output_folder, 'new_eff.eff')
    with zipfile.ZipFile(new_eff_file_path, 'w') as new_eff_zip:
        new_eff_zip.write(lst_file_path, 'eff.lst')
        new_eff_zip.write(new_dat_file_path, 'eff.dat')
    
    # Cleanup intermediate files and folders
    shutil.rmtree(dat_folder)
    os.remove(dat_file_path)
    os.remove(new_dat_file_path)
    
    print(f"New EFF package created at: {new_eff_file_path}")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process and amend an EFF package.")
    parser.add_argument("input_file", help="Path to the input .eff file.")
    parser.add_argument("output_folder", help="Folder to save the processed files.")
    args = parser.parse_args()
    
    # Call the processing function
    process_eff_package(args.input_file, args.output_folder)

if __name__ == "__main__":
    main()
