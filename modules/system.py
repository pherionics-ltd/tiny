import psutil
import platform
import json

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format - B, KB, MB, GB, TB, PB
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def collect_metrics_once():
    """
    Collects system metrics once and returns them as a dictionary.
    """
    # CPU usage (interval=None for near-instantaneous reading)
    cpu_percent = psutil.cpu_percent(interval=None) 
    cpu_count = psutil.cpu_count(logical=True)

    # Memory usage
    svmem = psutil.virtual_memory()
    memory_info = {
        "Total": get_size(svmem.total),
        "Available": get_size(svmem.available),
        "Used": get_size(svmem.used),
        "Percentage": f"{svmem.percent}%"
    }

    # Disk usage (for the root partition, modify as needed)
    disk_usage = psutil.disk_usage('/')
    disk_info = {
        "Total": get_size(disk_usage.total),
        "Used": get_size(disk_usage.used),
        "Free": get_size(disk_usage.free),
        "Percentage": f"{disk_usage.percent}%"
    }

    # Network I/O
    net_io = psutil.net_io_counters()
    network_info = {
        "Bytes Sent": get_size(net_io.bytes_sent),
        "Bytes Received": get_size(net_io.bytes_recv),
    }

    metrics = {
        "System": platform.system(),
        "CPU Cores": cpu_count,
        "CPU Usage": f"{cpu_percent}%",
        "Memory": memory_info,
        "Disk": disk_info,
        "Network": network_info
    }

    return metrics

if __name__ == "__main__":
    # Get metrics instantly and print the result in readable JSON format
    system_metrics = collect_metrics_once()
    print(json.dumps(system_metrics, indent=4))
