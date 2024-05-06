import os
import subprocess
import shutil

def main():
    # Get the current directory (USB drive)
    usb_drive = os.path.abspath(os.path.dirname(__file__))
    
    # Path to WinPMEM executable
    winpmem_path = os.path.join(usb_drive, 'winpmem.exe')
    
    # Destination path for saving memory dump
    dump_filename = 'memory_dump.raw'
    dump_path = os.path.join(usb_drive, dump_filename)
    
    # Run WinPMEM to acquire memory
    subprocess.run([winpmem_path, '-o', dump_path])
    
    # Verify if the dump file was created
    if os.path.isfile(dump_path):
        print(f"Memory dump saved successfully: {dump_path}")
    else:
        print("Memory dump creation failed.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

