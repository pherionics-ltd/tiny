import subprocess
import sys
import platform
import re

def tiny_ping(host, count=4):
    """
    Pings a host using the system's native ping command and parses the output.
    """
    # Determine the correct flag for the packet count based on the OS
    if platform.system().lower() == "windows":
        # Windows uses '-n' for count
        command = ['ping', '-n', str(count), host]
        # Regex pattern for Windows output: "Minimum = 10ms, Maximum = 12ms, Average = 11ms"
        avg_pattern = re.compile(r"Average = (\d+)ms")
    else:
        # Linux/macOS use '-c' for count
        command = ['ping', '-c', str(count), host]
        # Regex pattern for Linux/macOS output: "rtt min/avg/max/mdev = 1.234/5.678/9.012/3.456 ms"
        avg_pattern = re.compile(r"min/avg/max/mdev = [\d.]+/([\d.]+)/[\d.]+/[.d]+ ms")

    print(f"Pinging {host} with command: {' '.join(command)}")

    try:
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        output = result.stdout
        print(output)

        # Parse the output to find the average latency
        match = avg_pattern.search(output)
        if match:
            avg_latency = match.group(1)
            print(f"Summary: Average Latency to {host}: {avg_latency}ms")
            return float(avg_latency)
        else:
            print("Summary: Could not parse average latency from output.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error: Ping failed for host {host}")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: The 'ping' command was not found. Is it installed and in your PATH?")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if a hostname argument was provided
    if len(sys.argv) < 2:
        print("Usage: tiny tiny_ping <hostname_or_ip> [optional_ping_count]")
        sys.exit(1)

    host_target = sys.argv
    ping_count = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 4

    tiny_ping(host_target, count=ping_count)
