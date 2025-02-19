import subprocess
import threading
import signal
import sys

processes = []

def run_flask():
    flask_process = subprocess.Popen(["flask", "run", "--port", "5000"])
    processes.append(flask_process)
    flask_process.wait()

def run_streamlit():
    streamlit_process = subprocess.Popen(["streamlit", "run", "frontend.py"])
    processes.append(streamlit_process)
    streamlit_process.wait()

def cleanup_processes():
    for process in processes:
        if process.poll() is None:
            process.terminate()
            process.kill()

def run_both_apps():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    run_streamlit()
    flask_thread.join()

def handle_exit(sig, frame):
    cleanup_processes()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

if __name__ == "__main__":
    try:
        run_both_apps()
    except KeyboardInterrupt:
        cleanup_processes()
        sys.exit(0)
