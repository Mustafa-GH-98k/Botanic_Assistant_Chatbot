import subprocess
import threading

def run_flask():
    subprocess.run(["flask", "run", "--host=0.0.0.0", "--port=5000"])

def run_streamlit():
    subprocess.run(["streamlit", "run", "frontend.py", "--server.address", "0.0.0.0"])

def run_both_apps():
    run_flask()

if __name__ == "__main__":
    run_both_apps()
