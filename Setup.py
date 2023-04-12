import os
import sys
import time
import subprocess

def is_pip_installed():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
        return True
    except subprocess.CalledProcessError:
        return False

def install_pip():
    if is_pip_installed():
        print("pip is already installed.")
        return

    if sys.platform.startswith('win'):
        # Windows
        os.system("python -m ensurepip")
    else:
        # Unix-based systems (Linux, macOS)
        try:
            subprocess.check_call([sys.executable, '-m', 'ensurepip'])
        except subprocess.CalledProcessError:
            print("ensurepip is not available. Trying to install pip using get-pip.py.")
            try:
                from urllib.request import urlretrieve
            except ImportError:
                from urllib import urlretrieve

            get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
            urlretrieve(get_pip_url, "get-pip.py")

            try:
                subprocess.check_call([sys.executable, "get-pip.py"])
                os.remove("get-pip.py")
            except Exception as e:
                print("Error installing pip: {}".format(e))
                return

    if is_pip_installed():
        print("\npip has been installed successfully.")
        print("----------------------------------")
        time.sleep(2)
    else:
        print("\npip installation failed or is already present!")
        print("----------------------------------")
        time.sleep(2)

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

modules = ['openai', 'python-dotenv', 'PyPDF2']

if __name__ == "__main__":
    install_pip()

    for module in modules:
        try:
            install(module)
            print(f"\n{module} installed successfully.")
            print("----------------------------------")
        except Exception as e:
            print(f"Error installing {module}: {e}")
    time.sleep(5)
