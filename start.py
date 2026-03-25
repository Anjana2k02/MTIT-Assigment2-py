import subprocess
import threading
import sys
import os
import signal
import time
from urllib.request import urlopen

SERVICES = [
    {"name": "order-service",    "port": 8001, "dir": "order-service"},
    {"name": "menu-service",     "port": 8002, "dir": "menu-service"},
    {"name": "billing-service",  "port": 8003, "dir": "billing-service"},
    {"name": "table-service",    "port": 8004, "dir": "table-service"},
    {"name": "store-service",    "port": 8005, "dir": "store-service"},
    {"name": "delivery-service", "port": 8006, "dir": "delivery-service"},
    {"name": "user-service",      "port": 8007, "dir": "user-service"},
    {"name": "api-gateway",      "port": 8080, "dir": "api-gateway"},
]

# ANSI colors per service
COLORS = ["\033[96m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[91m", "\033[97m"]
RESET  = "\033[0m"

processes = []


def stream_output(proc, label, color):
    for line in iter(proc.stdout.readline, b""):
        print(f"{color}[{label}]{RESET} {line.decode(errors='replace').rstrip()}")


def _install_requirements(req_file):
    cmd = [sys.executable, "-m", "pip", "install", "-r", req_file]
    return subprocess.run(cmd, check=False)


def ensure_runtime_dependencies():
    try:
        import uvicorn  # noqa: F401
        import fastapi  # noqa: F401
        import beanie  # noqa: F401
        import motor  # noqa: F401
        import jose  # noqa: F401
        import email_validator  # noqa: F401
        return
    except ModuleNotFoundError:
        pass

    print("\033[93mMissing dependencies detected. Installing requirements for all services...\033[0m")
    for service in SERVICES:
        req_file = os.path.join(os.path.dirname(__file__), service["dir"], "requirements.txt")
        if not os.path.exists(req_file):
            continue

        print(f"\033[96mInstalling from {service['dir']}/requirements.txt...\033[0m")
        result = _install_requirements(req_file)
        if result.returncode != 0:
            print("\033[91mFailed to install dependencies. Please run manually:\033[0m")
            print(f"  {sys.executable} -m pip install -r {req_file}")
            sys.exit(result.returncode)

    try:
        import uvicorn  # noqa: F401
    except ModuleNotFoundError:
        print("\033[91muvicorn is still unavailable after installation.\033[0m")
        print(f"Please run: {sys.executable} -m pip install uvicorn[standard]")
        sys.exit(1)


def start_service(service, color):
    service_dir = os.path.join(os.path.dirname(__file__), service["dir"])
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", str(service["port"]),
        "--reload",
    ]
    proc = subprocess.Popen(
        cmd,
        cwd=service_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    processes.append(proc)
    thread = threading.Thread(target=stream_output, args=(proc, service["name"], color), daemon=True)
    thread.start()
    return proc


def wait_for_health(services, timeout_seconds=60):
    deadline = time.time() + timeout_seconds
    pending = {svc["name"]: svc["port"] for svc in services}

    while pending and time.time() < deadline:
        for name, port in list(pending.items()):
            try:
                with urlopen(f"http://localhost:{port}/health", timeout=2) as resp:
                    if resp.status == 200:
                        print(f"\033[92m[health]\033[0m {name} is healthy on :{port}")
                        del pending[name]
            except Exception:
                pass

        if pending:
            time.sleep(1)

    if pending:
        missing = ", ".join([f"{name}(:{port})" for name, port in pending.items()])
        print("\033[91mTimed out waiting for services to become healthy:\033[0m", missing)
        shutdown()


def shutdown(sig=None, frame=None):
    print("\n\033[91mShutting down all services...\033[0m")
    for proc in processes:
        proc.terminate()
    for proc in processes:
        proc.wait()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    ensure_runtime_dependencies()

    print("\033[1mStarting backend services first...\033[0m\n")
    backend_services = [s for s in SERVICES if s["name"] != "api-gateway"]
    gateway_service = next(s for s in SERVICES if s["name"] == "api-gateway")

    for i, service in enumerate(backend_services):
        color = COLORS[i % len(COLORS)]
        start_service(service, color)
        print(f"{color}[{service['name']}]{RESET} running on http://localhost:{service['port']}")

    print("\n\033[1mWaiting for backend services to become healthy...\033[0m")
    wait_for_health(backend_services)

    gateway_color = COLORS[len(backend_services) % len(COLORS)]
    print("\n\033[1mStarting API Gateway after backend readiness...\033[0m")
    start_service(gateway_service, gateway_color)
    print(f"{gateway_color}[{gateway_service['name']}]{RESET} running on http://localhost:{gateway_service['port']}")

    print("\n\033[1mAll services started. Press Ctrl+C to stop.\033[0m\n")

    # Keep main thread alive
    for proc in processes:
        proc.wait()
