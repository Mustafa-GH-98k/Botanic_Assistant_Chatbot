import subprocess
import threading
import signal
import sys

processes = []

def run_flask():
    gunicorn_process = subprocess.Popen(["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "--timeout", "300", "--log-file", "-", "app:app"])
    processes.append(gunicorn_process)
    gunicorn_process.wait()

def run_streamlit():
    streamlit_process = subprocess.Popen(["streamlit", "run", "frontend.py"])
    processes.append(streamlit_process)
    streamlit_process.wait()

def run_both_apps():
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.start()
    run_flask()
    streamlit_thread.join()


def kill_processes_on_port(port):
    print(f"Attempting to kill processes running on port {port}...")
    subprocess.run(["lsof", "-i", f":{port}", "-t"], stdout=subprocess.PIPE)
    pids = subprocess.run(["lsof", "-i", f":{port}", "-t"], stdout=subprocess.PIPE).stdout.decode().splitlines()
    print(f"Found the following processes: {pids}")
    for pid in pids:
        subprocess.run(["kill", pid])

cleanup_called = False

def cleanup(sig, frame):
    global cleanup_called
    if not cleanup_called:
        cleanup_called = True
        print("Cleaning up...")
        kill_processes_on_port(5000)
        print("Cleanup complete.")
        sys.exit(0)
    else:
        print("Cleanup already in progress, ignoring subsequent signals.")




def main():
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)  
    run_both_apps()

if __name__ == "__main__":
    main()