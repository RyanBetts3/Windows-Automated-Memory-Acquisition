import os
import subprocess
import ctypes

def run_as_admin():
    # Get the current script path
    script_path = os.path.abspath(__file__)
    
    # Run the script as administrator using ShellExecuteW
    ctypes.windll.shell32.ShellExecuteW(None, "runas", "winpmem.exe", '-o memory_dump.raw', None, 1)

def main():
    # Get the current directory (USB drive)
    usb_drive = os.path.abspath(os.path.dirname(__file__))
    
    # Check if winpmem.exe exists in the directory
    winpmem_path = os.path.join(usb_drive, 'winpmem.exe')
    if not os.path.isfile(winpmem_path):
        print("Error: winpmem.exe not found.")
        return
    
    # Destination path for saving memory dump
    dump_filename = 'memory_dump.raw'
    dump_path = os.path.join(usb_drive, dump_filename)
    
    # Run WinPMEM as administrator to acquire memory
    subprocess.run([winpmem_path, '-o', dump_path], shell=True, check=True)
    
    # Verify if the dump file was created
    if os.path.isfile(dump_path):
        print(f"Memory dump saved successfully: {dump_path}")
    else:
        print("Memory dump creation failed.")

if __name__ == "__main__":
    try:
        run_as_admin()
        main()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
