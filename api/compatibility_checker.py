def check_compatibility(cpu, ram, motherboard, gpu):
    issues = []

    # Set expected defaults
    expected_socket = "AM5"
    expected_ram_type = "DDR4"

    if motherboard:
        expected_socket = motherboard.get("socket", expected_socket)
        expected_ram_type = motherboard.get("ram_type", expected_ram_type)

    # CPU socket mismatch
    if cpu.get("socket") != expected_socket:
        issues.append("CPU socket may not match motherboard.")

    # RAM type mismatch
    if ram.get("ram_type") != expected_ram_type:
        issues.append("RAM type may not match motherboard.")

    # Handle GPU being a list or dict
    if isinstance(gpu, list):
        for g in gpu:
            if g and g.get("power_draw", 0) > 650:
                issues.append(f"GPU ({g.get('name')}) may require a higher wattage PSU.")
    elif isinstance(gpu, dict):
        if gpu.get("power_draw", 0) > 650:
            issues.append("GPU may require a higher wattage PSU.")

    return issues
