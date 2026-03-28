import psutil

def get_system_metrics():
    """Returns local system metrics for the admin panel"""
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        return {"cpu": cpu, "memory": memory, "disk": disk}
    except Exception:
        # Fallback if psutil fails or permissions missing
        return {"cpu": 0, "memory": 0, "disk": 0}
