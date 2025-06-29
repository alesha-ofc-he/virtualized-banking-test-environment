import subprocess

def configure_bridged_network(vm_name):
    return {"vm_name": vm_name, "network": "Bridged (simulated)", "ip": "192.168.1.100 (simulated)"}

def test_connectivity(vm_ip, target_ip="192.168.1.1"):
    try:
        result = subprocess.run(["ping", "-c", "4", target_ip], capture_output=True, text=True)
        return {"vm_ip": vm_ip, "target_ip": target_ip, "status": "Success" if result.returncode == 0 else "Failed", "output": result.stdout if result.returncode == 0 else result.stderr}
    except Exception as e:
        return {"vm_ip": vm_ip, "target_ip": target_ip, "status": f"Error: {e}"}