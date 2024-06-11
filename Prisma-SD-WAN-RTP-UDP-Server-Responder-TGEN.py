import subprocess
import os
import time
import shutil
import glob

# Define Git repository URL
script_repo_url = "https://github.com/khindaraj/Prisma-SD-WAN-RTP-UDP-Server-Responder-TGEN.git"

# Set working directory (replace with your actual directory)
working_directory = "/home/lab-user/scripts"

def make_scripts_executable(directory):
  """
  Makes downloaded .sh and .py files in the specified directory and its subdirectories executable.

  Args:
      directory: The directory to check for downloaded files.
  """
  for root, _, files in os.walk(directory):
    for filename in files:
      # Get the full path of the file
      filepath = os.path.join(root, filename)
      # Check if it's a file and the extension is .sh or .py
      if os.path.isfile(filepath) and (filename.endswith(".sh") or filename.endswith(".py")):
        # Make the file executable
        os.chmod(filepath, 0o755)  # Grant execute permission for owner, group, and others
        print(f"Made '{filepath}' executable")

# Manage script repository directory based on Git URL
def get_script_directory():
    """Returns the script directory based on the Git repository URL."""
    script_directory = os.path.join(working_directory, script_repo_url.split("/")[-1].split(".")[0])
    return script_directory


# Download or update scripts from the Git repository
def download_scripts():
    """Downloads the traffic generator scripts from the Git repository."""
    script_directory = get_script_directory()
    if not os.path.exists(script_directory):
        os.makedirs(script_directory)  # Create the directory if it doesn't exist
    subprocess.run(["git", "-C", script_directory, "pull"])  # Update existing directory
    if not os.path.isdir(script_directory):
        subprocess.run(["git", "clone", script_repo_url, script_directory])
    print("Scripts downloaded successfully.")


def install_dependencies():
    """Installs Python dependencies and Apache2 with the CGI module.

    This function checks if Python 3 and pip3 are available. If not, it
    installs them using the system's package manager (`apt`). Then, it
    installs the required Python libraries (`scapy`, `curl`) using pip3.
    Finally, it installs Apache2 with the CGI module using the package manager.

    Raises:
        RuntimeError: If there's an error during package installation.
    """

    # Check for Python 3 and pip3
    if not os.path.exists("/usr/bin/python3"):
        print("Installing Python 3...")
        try:
            subprocess.run(["apt", "get", "install", "-y", "python3"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error installing Python 3: {e}") from e

    if not os.path.exists("/usr/bin/pip3"):
        print("Installing pip3...")
        try:
            subprocess.run(["apt", "get", "install", "-y", "python3-pip"], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error installing pip3: {e}") from e

    # Install required Python libraries
    print("Installing scapy and curl...")
    try:
        subprocess.run(["pip3", "install", "scapy", "curl"], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error installing Python libraries: {e}") from e

    # Install Apache2 with CGI module
    print("Installing Apache2 with CGI module...")
    try:
        subprocess.run(["apt", "get", "install", "-y", "apache2-cgi"], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error installing Apache2 with CGI: {e}") from e

    print("Dependencies and Apache2 with CGI installed successfully!")

def copy_files_securely(script_dir, target_dir, files):
  """Copies files securely from a script directory to a target directory.

  Args:
      script_dir (str): The path to the directory containing the files to copy.
      target_dir (str): The path to the target directory where the files should be copied.
      files (list): A list of filenames to copy.

  Raises:
      ValueError: If the script or target directory doesn't exist or isn't writable.
      FileNotFoundError: If a specified file is not found in the script directory.
  """

  # Validate script directory existence and write permissions
  if not os.path.isdir(script_dir) or not os.access(script_dir, os.W_OK):
    raise ValueError(f"Script directory '{script_dir}' does not exist or is not writable.")

  # Validate target directory existence and write permissions
  if not os.path.isdir(target_dir) or not os.access(target_dir, os.W_OK):
    raise ValueError(f"Target directory '{target_dir}' does not exist or is not writable.")

  for filename in files:
    source_path = os.path.join(script_dir, filename)
    target_path = os.path.join(target_dir, filename)

    # Verify file existence in script directory
    if not os.path.isfile(source_path):
      raise FileNotFoundError(f"File '{filename}' not found in script directory.")

    # Use shutil.copy2 to preserve file metadata (optional)
    shutil.copy2(source_path, target_path)  # Use shutil.copy() for basic copying

  print(f"Files copied successfully to '{target_dir}'.")

def create_systemd_service(script_name="udp_echo", script_pattern="*.sh", script_dir="/root/scripts"):
  """Creates a systemd service file to launch the first matching script from a directory.

  Args:
      script_name (str, optional): Desired service name (defaults to "udp_echo").
      script_pattern (str, optional): Glob pattern to find the script (defaults to "*.sh").
      script_dir (str, optional): Directory containing the script to be launched (defaults to "/root/scripts").

  Raises:
      ValueError: If no matching script is found in the specified directory.
  """

  # Find script path using glob
  script_path = glob.glob(os.path.join(script_dir, script_pattern))[0]
  if not script_path:
    raise ValueError(f"No script found matching '{script_pattern}' in '{script_dir}'.")

  # Create the service content
  service_content = f"""
[Unit]
Description=UDP Echo Script - {script_path}
After=network.target

[Service]
Type=simple
User=rtp_user  # Replace with a dedicated user (recommended)
WorkingDirectory={os.path.dirname(script_path)}  # Script directory
ExecStart={script_path} &  # Launch script in the background
StandardOutput=syslog
StandardError=syslog
SyslogLevel=info

[Install]
WantedBy=multi-user.target
"""

  service_file_path = f"/etc/systemd/system/{script_name}.service"

  with open(service_file_path, "w") as f:
    f.write(service_content)

  print(f"Systemd service file created: {service_file_path}")


def main():
    """Main function for script execution."""
    
    target_dir = "/usr/lib/cgi-bin"  # Consider security implications before using this directory
    files = ["hw.sh", "get_env.sh"]
    
    script_directory = get_script_directory()

    # Download scripts (replace with your actual implementation)
    download_scripts()

    # Install dependencies (replace with your actual implementation)
    install_dependencies()
    
    os.chdir(working_directory)  # Change the current working directory

    # Make downloaded scripts executable in all subdirectories
    make_scripts_executable(working_directory)  

    # Ensure you understand the security risks before copying to /usr/lib/cgi-bin
    copy_files_securely(script_directory, target_dir, files)
    
    create_systemd_service(script_name="udp_echo", script_pattern="udp_echo.sh", script_dir=script_directory)
    
    print("Scripts downloaded, dependencies installed, and systemd services started.")

if __name__ == "__main__":
    main()

