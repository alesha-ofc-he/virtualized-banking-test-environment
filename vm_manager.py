from pyvmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import ssl
import time

def connect_vmware(host="localhost", user="your_username", password="your_password"):
    context = ssl._create_unverified_context()
    try:
        si = SmartConnect(host=host, user=user, pwd=password, port=443, sslContext=context)
        return si
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def create_vm(si, vm_name="BankTestServer", cpu=2, ram_mb=4096, disk_gb=20):
    if not si:
        return {"vm_name": vm_name, "status": "Failed: No connection"}
    content = si.RetrieveContent()
    datacenter = content.rootFolder.childEntity[0]
    vm_folder = datacenter.vmFolder
    resource_pool = datacenter.hostFolder.childEntity[0].resourcePool
    vm_spec = vim.vm.ConfigSpec(
        name=vm_name, memoryMB=ram_mb, numCPUs=cpu, guestId="windows9Server64Guest"
    )
    task = vm_folder.CreateVM_Task(config=vm_spec, pool=resource_pool)
    print(f"Creating VM: {vm_name}")
    while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
        time.sleep(1)
    if task.info.state == vim.TaskInfo.State.success:
        return {"vm_name": vm_name, "status": "Created"}
    return {"vm_name": vm_name, "status": f"Failed: {task.info.error}"}

def create_snapshot(si, vm_name, snapshot_name):
    if not si:
        return {"vm_name": vm_name, "status": "Failed: No connection"}
    content = si.RetrieveContent()
    vm = next((child for child in content.rootFolder.childEntity[0].vmFolder.childEntity if child.name == vm_name), None)
    if vm:
        task = vm.CreateSnapshot_Task(name=snapshot_name, description=f"Snapshot created on {time.strftime('%Y-%m-%d %H:%M:%S')}", memory=False, quiesce=False)
        while task.info.state not in [vim.TaskInfo.State.success, vim.TaskInfo.State.error]:
            time.sleep(1)
        return {"vm_name": vm_name, "status": "Snapshot created" if task.info.state == vim.TaskInfo.State.success else f"Snapshot failed: {task.info.error}"}
    return {"vm_name": vm_name, "status": "VM not found"}