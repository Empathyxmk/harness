import time
import json

def wait_for_gunicorn(container, sleep_time=0.1, timeout=5):
    """Wait for gunicorn to appear in process list inside container."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            processes = container.top()["Processes"]
            for proc in processes:
                if "gunicorn" in proc[-1]:
                    return True
        except Exception:
            pass
        time.sleep(sleep_time)
    return False

def get_config_from_container(container, config_path):
    try:
        output = container.exec_run(f"cat {config_path}").output
        return json.loads(output.decode())
    except Exception:
        return None

def print_container_logs(container):
    print("Container logs:", container.logs().decode())

def cleanup_container(container):
    # Simulate cleaning up a container (stop and remove)
    container.stop()
    container.remove()

# ---- Missing functions for legacy tests in test_utils.py ----

def get_process_names(container):
    """Extract process command lines from container's top info."""
    # Change: Only return gunicorn processes
    return [proc[-1] for proc in container.top()["Processes"] if "gunicorn" in proc[-1]]

def get_gunicorn_conf_path(container):
    """Extract the gunicorn config file path from gunicorn process cmdline."""
    procs = container.top()["Processes"]
    gunicorn_proc = [p for p in procs if "gunicorn" in p[-1]][0]
    parts = gunicorn_proc[-1].split()
    if "-c" in parts:
        return parts[parts.index("-c") + 1]
    raise IndexError("No -c found in gunicorn cmdline")

def get_config(container):
    """Extract config from container using JSON output via exec_run."""
    output = container.exec_run("cat /config.json").output
    return json.loads(output.decode())

def remove_previous_container(client):
    """Remove previous container if found, else ignore NotFound."""
    try:
        container = client.containers.get("main_container")
        container.stop()
        container.remove()
    except Exception:
        return None

def get_logs(container):
    """Return UTF-8-decoded logs from container."""
    return container.logs().decode("utf-8")

def get_response_text1():
    """Synthesize a response message using the PYTHON_VERSION env var."""
    import os
    version = os.environ.get("PYTHON_VERSION", "unknown")
    return f"Hello World running Python {version}!"