import subprocess
import threading

def run_flask():
    subprocess.run(["flask", "run", "--port", "5000"])

def run_streamlit():
    subprocess.run(["streamlit", "run", "frontend.py"])

def run_both_apps():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    run_streamlit()

if __name__ == "__main__":
    run_both_apps()
