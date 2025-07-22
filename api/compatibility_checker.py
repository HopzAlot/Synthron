def check_compatibility(cpu, ram, motherboard, gpu):
    issues = []

    # Set expected defaults
    expected_socket = "AM5"
    expected_ram_type = "DDR4"

    if motherboard:
        expected_socket = motherboard.get("socket", expected_socket)
        expected_ram_type = motherboard.get("ram_type", expected_ram_type)
    else:
        issues.append("Motherboard info is missing, socket and RAM type checks may be inaccurate.")

    # CPU socket mismatch
    if cpu and cpu.get("socket") is not None and cpu.get("socket") != expected_socket:
        issues.append("CPU socket may not match motherboard.")

    # RAM type mismatch
    if ram and ram.get("ram_type") is not None and ram.get("ram_type") != expected_ram_type:
        issues.append("RAM type may not match motherboard.")

    # GPU power draw check (handle list or single GPU)
    if isinstance(gpu, list):
        for g in gpu:
            if g and g.get("power_draw") is not None and g.get("power_draw", 0) > 650:
                issues.append(f"GPU ({g.get('name', 'Unknown')}) may require a higher wattage PSU.")
    elif isinstance(gpu, dict):
        if gpu.get("power_draw") is not None and gpu.get("power_draw", 0) > 650:
            issues.append(f"GPU ({gpu.get('name', 'Unknown')}) may require a higher wattage PSU.")
    elif gpu is None:
        issues.append("GPU info is missing.")

    return issues