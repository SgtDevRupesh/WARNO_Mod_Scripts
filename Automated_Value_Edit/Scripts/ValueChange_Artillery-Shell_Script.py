import re
import os

# Define input/output file paths
unite_descriptor_input = r"C:\Users\SgtDevRupesh_MW\Downloads\WARNO_Modding\Automated_Value_Edit\Original_Files\UniteDescriptor.txt"
weapon_descriptor_input = r"C:\Users\SgtDevRupesh_MW\Downloads\WARNO_Modding\Automated_Value_Edit\Original_Files\WeaponDescriptor.txt"
ammunition_input = r"C:\Users\SgtDevRupesh_MW\Downloads\WARNO_Modding\Automated_Value_Edit\Original_Files\Ammunition.txt"
ammunition_output = r"C:\Users\SgtDevRupesh_MW\Downloads\WARNO_Modding\Automated_Value_Edit\Modified_Files\Ammunition_Modified.txt"
log_path = r"C:\Users\SgtDevRupesh_MW\Downloads\WARNO_Modding\Automated_Value_Edit\Logs\Artillery_Modification_Logs.txt"

# Important variables for scanning units, weapons, and ammunition
acknow_unit_type_value = "~/TAcknowUnitType_ArtShell"
acknow_unit_type_key = "AcknowUnitType"
weapon_manager_default_key = "WeaponManager"
default_weapon_key = "Default"
ammunition_key = "Ammunition"

# Custom unit and value declaration
UseCustomTable = False  # If false, the script does not use the custom table
CustomTable_DirectValueUsed = False  # If true, the script uses direct values; otherwise, it uses multipliers
Disable_Smoke_Ammo = True  # Prevents modification of smoke-based ammo

CustomTable_DirectValue = [
    # ("UnitName", RadiusSplashPhysicalDamage, PhysicalDamage, RadiusSplashSuppressDamage, SuppressDamage)
    #("Ammo_Howz_Canon_2A18_Howitzer_122mm", 200, 2.5, 300, 170),  # Example custom direct values
]

CustomTable_Multipliers = [
    # ("UnitName", RadiusSplashPhysicalDamage_Multiplier, PhysicalDamage_Multiplier, RadiusSplashSuppressDamage_Multiplier, SuppressDamage_Multiplier)
    #("Ammo_Howz_Canon_2A18_Howitzer_122mm", 2.0, 1.8, 1.7, 1.6),  # Example custom multipliers
]

# Ammunition stat variables
RadiusSplashPhysicalDamage = "RadiusSplashPhysicalDamages"
PhysicalDamage = "PhysicalDamages"
RadiusSplashSuppressDamage = "RadiusSplashSuppressDamages"
SuppressDamage = "SuppressDamages"

# Multipliers for ammunition stats
RadiusSplashPhysicalDamage_Multiplier = 1.5
PhysicalDamage_Multiplier = 1.5
RadiusSplashSuppressDamage_Multiplier = 1.5
SuppressDamage_Multiplier = 1.5

# Helper function to strip prefixes
def strip_prefix(value):
    return value.split('/')[-1]

# Function to write clean logs
def log_message(message, log_file):
    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(message + "\n")

# Function to check if the ammunition is smoke-based
def is_smoke_ammo(ammo_name):
    with open(ammunition_input, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    inside_ammo_block = False
    parentheses_counter = 0

    for i, line in enumerate(lines):
        if f"{ammo_name} is TAmmunitionDescriptor" in line:
            inside_ammo_block = True
            parentheses_counter = 1  # Start of the block

        if inside_ammo_block:
            if '(' in line:
                parentheses_counter += 1
            if ')' in line:
                parentheses_counter -= 1

            if "SmokeDescriptor" in line:
                return 'nil' not in line  # True if it's smoke-based

            if parentheses_counter == 0:
                break  # End of the block

    return False  # Default return if no SmokeDescriptor found

# Function to find artillery units and their weapons
def find_artillery_units_and_weapons():
    with open(unite_descriptor_input, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    inside_artillery_unit = False
    weapon_names = []

    for i, line in enumerate(lines):
        # Identify the line where the artillery unit starts
        if acknow_unit_type_value in line:
            inside_artillery_unit = True
            unit_line = i + 1  # Capture the line number of the artillery unit
            #log_message(f"Artillery unit found at line {unit_line}", log_path)

        # Continue scanning for the associated weapon name within the artillery unit
        if inside_artillery_unit and weapon_manager_default_key in line:
            continue

        # Look for weapon descriptors within the artillery unit block
        if inside_artillery_unit and "/GFX/Weapon/" in line:
            weapon_name = strip_prefix(line.split('=')[-1].strip())
            weapon_names.append((weapon_name, unit_line))
            #log_message(f"Weapon found: {weapon_name} at line {unit_line}", log_path)
            inside_artillery_unit = False  # Reset after finding the weapon

    return weapon_names

# Enhanced Function to find all ammunition from WeaponDescriptor
def find_ammunition(weapon_name):
    with open(weapon_descriptor_input, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    ammunitions = []
    inside_weapon_block = False
    inside_mounted_weapon_list = False
    inside_mounted_weapon = False

    for i, line in enumerate(lines):
        if f"export {weapon_name} is TWeaponManagerModuleDescriptor" in line:
            inside_weapon_block = True
            log_message(f"Found WeaponDescriptor block for {weapon_name} at line {i}", log_path)

        if inside_weapon_block and ")" in line and not inside_mounted_weapon_list:
            inside_weapon_block = False

        if inside_weapon_block and "MountedWeaponDescriptorList" in line:
            inside_mounted_weapon_list = True
            continue

        if inside_mounted_weapon_list and "TMountedWeaponDescriptor" in line:
            inside_mounted_weapon = True
            continue

        if inside_mounted_weapon and "Ammunition" in line:
            ammo_name = strip_prefix(line.split('=')[-1].strip())
            ammunitions.append(ammo_name)
            log_message(f"Found ammunition: {ammo_name} at line {i}", log_path)

        if inside_mounted_weapon and "AdditionalAmmunitions" in line:
            ammo_name = strip_prefix(line.split('=')[-1].strip())
            ammunitions.append(ammo_name)
            log_message(f"Found additional ammunition: {ammo_name} at line {i}", log_path)

        if inside_mounted_weapon and ")" in line:
            inside_mounted_weapon = False

        if inside_mounted_weapon_list and not inside_mounted_weapon and "]" in line:
            inside_mounted_weapon_list = False

    if not ammunitions:
        log_message(f"No ammunitions found for weapon {weapon_name}", log_path)
        
    return ammunitions if ammunitions else []

# Function to check if a unit is in the custom table and apply values or multipliers
def check_custom_table(unit_name, stat_name, original_value):
    new_value = original_value

    if CustomTable_DirectValueUsed:
        for entry in CustomTable_DirectValue:
            if entry[0] == unit_name:
                stat_index = [RadiusSplashPhysicalDamage, PhysicalDamage, RadiusSplashSuppressDamage, SuppressDamage].index(stat_name)
                if entry[stat_index + 1] is not None:
                    return entry[stat_index + 1]

    else:
        for entry in CustomTable_Multipliers:
            if entry[0] == unit_name:
                stat_index = [RadiusSplashPhysicalDamage, PhysicalDamage, RadiusSplashSuppressDamage, SuppressDamage].index(stat_name)
                if entry[stat_index + 1] is not None:
                    return original_value * entry[stat_index + 1]

    if stat_name == RadiusSplashPhysicalDamage:
        new_value = original_value * RadiusSplashPhysicalDamage_Multiplier
    elif stat_name == PhysicalDamage:
        new_value = original_value * PhysicalDamage_Multiplier
    elif stat_name == RadiusSplashSuppressDamage:
        new_value = original_value * RadiusSplashSuppressDamage_Multiplier
    elif stat_name == SuppressDamage:
        new_value = original_value * SuppressDamage_Multiplier

    return new_value

# Function to log changes
def log_change(ammo_name, stat_name, original_value, new_value, log_file):
    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(f"  -> {ammo_name}: {stat_name} modified from {original_value} to {new_value}\n")

# Function to modify ammunition
def modify_ammunition(ammo_name):
    with open(ammunition_input, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = []
    inside_ammo_block = False
    modification_done = set()

    if Disable_Smoke_Ammo and is_smoke_ammo(ammo_name):
        log_message(f"{ammo_name} is smoke-based, skipping modification", log_path)
        return

    damage_keys = {
        RadiusSplashPhysicalDamage: RadiusSplashPhysicalDamage_Multiplier,
        PhysicalDamage: PhysicalDamage_Multiplier,
        RadiusSplashSuppressDamage: RadiusSplashSuppressDamage_Multiplier,
        SuppressDamage: SuppressDamage_Multiplier,
    }

    for i, line in enumerate(lines):
        if f"{ammo_name} is TAmmunitionDescriptor" in line:
            log_message(f"Found the start of {ammo_name} block at line {i}", log_path)
            inside_ammo_block = True

        if inside_ammo_block:
            for damage_key in [RadiusSplashPhysicalDamage, PhysicalDamage, RadiusSplashSuppressDamage, SuppressDamage]:
                if damage_key in line and damage_key not in modification_done:
                    match = re.search(r'([\d.]+)', line)
                    
                    if match:
                        original_value = float(match.group(1))
                        new_value = check_custom_table(ammo_name, damage_key, original_value)
                        
                        line = line.replace(match.group(1), str(new_value))
                        log_change(ammo_name, damage_key, original_value, new_value, log_path)
                        modification_done.add(damage_key)

        if inside_ammo_block and ")" in line and modification_done:
            log_message(f"Completed processing block for {ammo_name} at line {i}", log_path)
            inside_ammo_block = False

        updated_lines.append(line)

    with open(ammunition_output, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)

# Main function to orchestrate the process
def main():
    log_message("========== Processing Start ==========", log_path)
    weapon_names = find_artillery_units_and_weapons()
    
    for set_num, (weapon, unit_line) in enumerate(weapon_names, 1):
        log_message(f"========== SET {set_num} ==========", log_path)
        #log_message(f"Artillery Unit found at line {unit_line}", log_path)
        #log_message(f"Weapon: {weapon}", log_path)

        ammunitions = find_ammunition(weapon)
        if ammunitions:
            log_message(f"Ammunitions for {weapon}: {ammunitions}", log_path)
            for ammo in ammunitions:
                log_message(f"Modifying ammunition: {ammo}", log_path)
                modify_ammunition(ammo)
        log_message("", log_path)

    log_message("========== Processing Complete ==========", log_path)

if __name__ == "__main__":
    main()
