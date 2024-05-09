
import streamlit as st
import subprocess
import os
import shutil
import time

# Define the directory for the app and a temporary directory for uploads
app_dir = os.getcwd()  # Main directory where the app is running
temp_dir = os.path.join(app_dir, 'temp')

# Create or clean the temporary directory at the start of the session
if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
os.makedirs(temp_dir)

# Streamlit app interface
st.title("Molecule Configuration Tool")

# Upload files
mol2_file = st.file_uploader("Upload a .mol2 file", type=['mol2'])
str_file = st.file_uploader("Upload a .str file", type=['str'])

# Text input for molecule name
molecule_name = st.text_input("Enter the molecule name")

# Function to list and download files from the main app directory
def list_and_download_files(directory):
    time.sleep(2)  # Wait to ensure all files have been written
    files = os.listdir(directory)
    if files:
        st.write("Output files detected:")
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):  # Check if it's a file and not a directory
                st.write(file)  # Log the detected files
                with open(file_path, "rb") as f:
                    st.download_button(label=f"Download {file}", data=f, file_name=file, mime='application/octet-stream')
    else:
        st.error("No output files found. Please check the script execution details.")

# Button to execute the script
if st.button("Run Script"):
    uploaded_files = [mol2_file.name if mol2_file else None, str_file.name if str_file else None]
    if mol2_file and str_file and molecule_name:
        # Save uploaded files to the temporary directory
        mol2_path = os.path.join(temp_dir, mol2_file.name)
        with open(mol2_path, "wb") as f:
            f.write(mol2_file.getvalue())
        
        str_path = os.path.join(temp_dir, str_file.name)
        with open(str_path, "wb") as f:
            f.write(str_file.getvalue())

        # Command to execute the script
        cmd = [
            'python3', 'cgenff_charmm2gmx.py', molecule_name,
            mol2_path, str_path, 'charmm36-jul2022.ff'
        ]

        try:
            # Execute the command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            st.success("Script executed successfully!")
            st.code(result.stdout)
            
            # List and offer downloads for output files detected in the app directory
            list_and_download_files(app_dir)
        except subprocess.CalledProcessError as e:
            st.error("Failed to execute script")
            st.code(e.stderr)
    else:
        st.error("Please upload both files and set the molecule name.")
