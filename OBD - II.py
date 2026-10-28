import time

def decode_rpm(a_hex, b_hex):
    # Formula: ((A * 256) + B) / 4
    a = int(a_hex, 16)
    b = int(b_hex, 16)
    return int(((a * 256) + b) / 4)

def decode_speed(a_hex):
    # Formula: A (in km/h)
    return int(a_hex, 16)

def decode_coolant_temp(a_hex):
    # Formula: A - 40 (in °C)
    return int(a_hex, 16) - 40


def parse_obd_frame(hex_string):
    # Clean up input string
    bytes_list = hex_string.strip().split()
    
    # Basic check to see if it's a valid message
    if len(bytes_list) < 3:
        return "Invalid Frame"

    mode = bytes_list[0]  # Mode 41 = Live Telemetry Response
    pid = bytes_list[1]   # Parameter ID (What sensor it is)

    if mode == "41":
        if pid == "0C":   # Engine RPM
            rpm = decode_rpm(bytes_list[2], bytes_list[3])
            return f"🟢 [RPM Sensor]: {rpm} RPM"
        elif pid == "0D": # Vehicle Speed
            speed = decode_speed(bytes_list[2])
            return f"🔵 [Speedometer]: {speed} km/h"
        elif pid == "05": # Coolant Temp
            temp = decode_coolant_temp(bytes_list[2])
            return f"🔴 [Coolant Temp]: {temp} °C"

    return "Unknown/Unsupported PID Frame"


# --- MOCK TELEMETRY TEST RUN ---
if __name__ == "__main__":
    print("=== OBD-II LOG PARSER ===")
    print("Decoding raw telemetry frames...\n")

    # Sample raw ECU hex logs
    raw_logs = [
        "41 0C 1A F0",  # RPM frame (~1724 RPM)
        "41 0D 4B",     # Speed frame (75 km/h)
        "41 05 78",     # Coolant temp frame (80 °C)
        "41 0C 3E 80",  # High RPM frame (~4000 RPM)
    ]

    for frame in raw_logs:
        result = parse_obd_frame(frame)
        print(f"Raw Input: '{frame}'  -->  {result}")
        time.sleep(0.5)