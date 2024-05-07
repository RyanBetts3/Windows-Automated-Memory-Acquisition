import os
import sys
import subprocess
import ctypes
import logging
from tkinter import Tk, filedialog, messagebox

# Configure logging
logging.basicConfig(filename='memory_acquisition.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_admin():
    """
    Check if the script is running with administrative privileges.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logging.error(f"Failed to check administrative privileges: {str(e)}")
        return False

def run_as_admin():
    """
    Attempt to run the script with administrative privileges.
    """
    if not is_admin():
        try:
            script_path = os.path.abspath(__file__)
            params = ' '.join(sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f"{script_path} {params}", None, 1)
        except Exception as e:
            logging.error(f"Failed to run the script with administrative privileges: {str(e)}")
        sys.exit(1)

def acquire_memory_dump(output_path):
    """
    Acquire memory dump using WinPMEM.
    """
    winpmem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'winpmem.exe')
    if not os.path.isfile(winpmem_path):
        logging.error("Error: winpmem.exe not found.")
        return False

    try:
        logging.info("Starting memory acquisition...")
        subprocess.run([winpmem_path, '-o', output_path], check=True)
        logging.info(f"Memory dump saved successfully: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Memory acquisition failed with error code {e.returncode}")
    except Exception as e:
        logging.error(f"An error occurred during memory acquisition: {str(e)}")

    return False

def main():
    """
    Main function to run the memory acquisition script.
    """
    run_as_admin()

    root = Tk()
    root.withdraw()

    usb_drive = filedialog.askdirectory(title="Select USB Drive")
    if not usb_drive:
        logging.error("No USB drive selected.")
        return

    dump_filename = filedialog.asksaveasfilename(initialdir=usb_drive, title="Save Memory Dump", defaultextension=".raw", filetypes=[("Raw Memory Dump", "*.raw")])
    if not dump_filename:
        logging.error("No output file selected.")
        return

    if acquire_memory_dump(dump_filename):
        messagebox.showinfo("Memory Acquisition", "Memory dump acquired successfully.")
    else:
        messagebox.showerror("Memory Acquisition", "Failed to acquire memory dump.")

    root.destroy()

if __name__ == "__main__":
    main()