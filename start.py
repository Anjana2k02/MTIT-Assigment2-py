import subprocess
import threading
import sys
import os
import signal
import time
import socket
from urllib.request import urlopen

SERVICES = [
    {"name": "menu-service",     "port": 8002, "dir": "menu-service"},
    {"name": "billing-service",  "port": 8003, "dir": "billing-service"},
    {"name": "table-service",    "port": 8004, "dir": "table-service"},
    {"name": "store-service",    "port": 8005, "dir": "store-service"},
    {"name": "delivery-service", "port": 8006, "dir": "delivery-service"},
    {"name": "user-service",      "port": 8007, "dir": "user-service", "health_path": "/"},
    {"name": "api-gateway",      "port": 8081, "dir": "api-gateway"},
]

SERVICE_URL_ENV_MAP = {
    "order-service": "ORDER_SERVICE_URL",
    "menu-service": "MENU_SERVICE_URL",
    "billing-service": "BILLING_SERVICE_URL",
    "table-service": "TABLE_SERVICE_URL",
    "store-service": "STORE_SERVICE_URL",
    "delivery-service": "DELIVERY_SERVICE_URL",
    "user-service": "USER_SERVICE_URL",
}

# ANSI colors per service
COLORS = ["\033[96m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[91m", "\033[97m"]
RESET  = "\033[0m"

processes = []
ENABLE_RELOAD = os.environ.get("DEV_RELOAD", "0") == "1"


def load_root_env() -> None:
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


def stream_output(proc, label, color):
    for line in iter(proc.stdout.readline, b""):
        print(f"{color}[{label}]{RESET} {line.decode(errors='replace').rstrip()}")


def _install_requirements(req_file):
    cmd = [sys.executable, "-m", "pip", "install", "-r", req_file]
    return subprocess.run(cmd, check=False)


def _is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _find_available_port(preferred_port, max_offset=50, reserved_ports=None):
    reserved_ports = reserved_ports or set()
    for port in range(preferred_port, preferred_port + max_offset + 1):
        if port in reserved_ports:
            continue
        if not _is_port_in_use(port):
            return port
    raise RuntimeError(
        f"No available port found in range {preferred_port}-{preferred_port + max_offset}."
    )


def resolve_service_ports(services):
    resolved = []
    reserved_ports = set()
    for service in services:
        desired_port = service["port"]
        actual_port = _find_available_port(desired_port, reserved_ports=reserved_ports)
        service_copy = dict(service)
        service_copy["port"] = actual_port
        resolved.append(service_copy)
        reserved_ports.add(actual_port)

        if actual_port != desired_port:
            print(
                "\033[93mPort in use:\033[0m "
                f"{service['name']} requested :{desired_port}, using :{actual_port}"
            )
    return resolved


def apply_service_url_env(services):
    for service in services:
        env_var = SERVICE_URL_ENV_MAP.get(service["name"])
        if not env_var:
            continue
        os.environ[env_var] = f"http://localhost:{service['port']}"


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
    ]
    if ENABLE_RELOAD:
        cmd.append("--reload")
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
    pending = {
        svc["name"]: {
            "port": svc["port"],
            "health_path": svc.get("health_path", "/health"),
        }
        for svc in services
    }

    while pending and time.time() < deadline:
        for name, meta in list(pending.items()):
            port = meta["port"]
            health_path = meta["health_path"]
            try:
                with urlopen(f"http://localhost:{port}{health_path}", timeout=2) as resp:
                    if 200 <= resp.status < 400:
                        print(f"\033[92m[health]\033[0m {name} is healthy on :{port}")
                        del pending[name]
            except Exception:
                pass

        if pending:
            time.sleep(1)

    if pending:
        missing = ", ".join([
            f"{name}(:{meta['port']}, check {meta['health_path']})"
            for name, meta in pending.items()
        ])
        print("\033[91mTimed out waiting for services to become healthy:\033[0m", missing)
        shutdown(exit_code=1)


def shutdown(sig=None, frame=None, exit_code=0):
    print("\n\033[91mShutting down all services...\033[0m")
    for proc in processes:
        proc.terminate()
    for proc in processes:
        proc.wait()
    sys.exit(exit_code)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    load_root_env()
    ensure_runtime_dependencies()

    if ENABLE_RELOAD:
        print("\033[93mDEV_RELOAD=1 detected: uvicorn auto-reload is enabled.\033[0m")
    else:
        print("\033[92mRunning without auto-reload for stable multi-service startup.\033[0m")

    print("\033[1mStarting backend services first...\033[0m\n")
    backend_services = [s for s in SERVICES if s["name"] != "api-gateway"]
    gateway_service = next(s for s in SERVICES if s["name"] == "api-gateway")

    resolved_backend_services = resolve_service_ports(backend_services)
    apply_service_url_env(resolved_backend_services)

    resolved_gateway_service = dict(gateway_service)
    reserved_backend_ports = {service["port"] for service in resolved_backend_services}
    resolved_gateway_service["port"] = _find_available_port(
        gateway_service["port"],
        reserved_ports=reserved_backend_ports,
    )
    if resolved_gateway_service["port"] != gateway_service["port"]:
        print(
            "\033[93mPort in use:\033[0m "
            f"api-gateway requested :{gateway_service['port']}, using :{resolved_gateway_service['port']}"
        )

    for i, service in enumerate(resolved_backend_services):
        color = COLORS[i % len(COLORS)]
        start_service(service, color)
        print(f"{color}[{service['name']}]{RESET} running on http://localhost:{service['port']}")

    print("\n\033[1mWaiting for backend services to become healthy...\033[0m")
    wait_for_health(resolved_backend_services)

    gateway_color = COLORS[len(resolved_backend_services) % len(COLORS)]
    print("\n\033[1mStarting API Gateway after backend readiness...\033[0m")
    start_service(resolved_gateway_service, gateway_color)
    print(
        f"{gateway_color}[{resolved_gateway_service['name']}]{RESET} "
        f"running on http://localhost:{resolved_gateway_service['port']}"
    )

    print("\n\033[1mAll services started. Press Ctrl+C to stop.\033[0m\n")

    # Keep main thread alive
    for proc in processes:
        proc.wait()
