from vm_manager import connect_vmware, create_vm, create_snapshot
from network_utils import configure_bridged_network, test_connectivity
from database import init_db, log_report
import datetime
import os

def run_test_environment(vm_name="BankTestServer", snapshot_name="InitialSnapshot"):
    init_db()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    si = connect_vmware(host="localhost", user="your_username", password="your_password")
    if not si:
        print("Failed to connect to VMware")
        return
    vm_result = create_vm(si, vm_name=vm_name, cpu=2, ram_mb=4096, disk_gb=20)
    print(f"VM Creation: {vm_result}")
    network_result = configure_bridged_network(vm_name)
    print(f"Network Configuration: {network_result}")
    connectivity_result = test_connectivity(vm_ip=network_result["ip"], target_ip="192.168.1.1")
    print(f"Connectivity Test: {connectivity_result}")
    snapshot_result = create_snapshot(si, vm_name, snapshot_name)
    print(f"Snapshot: {snapshot_result}")
    report_data = {
        "timestamp": timestamp,
        "vm_name": vm_name,
        "vm_status": vm_result["status"],
        "network_status": network_result["network"],
        "connectivity_status": connectivity_result["status"]
    }
    log_report(report_data)
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/report_{timestamp.replace(':', '-')}.txt"
    with open(report_path, "w") as f:
        f.write(f"Virtualized Banking Test Environment Report - {timestamp}\n")
        f.write(f"VM Name: {vm_name}\n")
        f.write(f"VM Status: {vm_result['status']}\n")
        f.write(f"Network: {network_result['network']}\n")
        f.write(f"Connectivity: {connectivity_result['status']}\n")
        f.write(f"Snapshot: {snapshot_result['status']}\n")
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    run_test_environment()