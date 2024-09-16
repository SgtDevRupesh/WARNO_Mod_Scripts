import re
import os

# File paths for the vehicle data
uniteDescriptor_path = r"C:\Users\SgtDevRupesh_MW\Downloads\WARNO_Modding\Automated_Value_Edit\Original_Files\UniteDescriptor.txt"
uniteDescriptor_Modified_path = r"C:\Users\SgtDevRupesh_MW\Downloads\WARNO_Modding\Automated_Value_Edit\Modified_Files\UniteDescriptor_Modified.txt"

# Configurable variable names
speed_key = "MaxSpeedInKmph"  # Can be updated if the game devs change the variable name
supply_key = "SupplyCapacity"  # Can be updated if the game devs change the variable name
fuel_key = "FuelCapacity"  # Can be updated if the game devs change the variable name

# Configurable behavior
speed_divide = True  # If True, speed will be divided. If False, it will be multiplied.
supply_multiply = True  # If True, supply will be multiplied. If False, it will be divided.
fuel_multiply = True  # If True, fuel will be multiplied. If False, it will be divided.

# Configurable factors
speed_factor = 1.25  # Factor for speed modification
supply_factor = 2  # Factor for supply capacity modification
fuel_factor = 2  # Factor for fuel capacity modification

# Open the file containing the vehicle data
with open(uniteDescriptor_path, 'r') as file:
    data = file.read()

# Function to update speed based on the `speed_divide` flag
def update_speed(match):
    original_speed = float(match.group(1))  # Get the original speed as a float
    if speed_divide:
        new_speed = int(original_speed / speed_factor)  # Divide if the flag is set
    else:
        new_speed = int(original_speed * speed_factor)  # Multiply otherwise
    # Return the updated line with a comment showing the original and new speeds using //
    return f'{speed_key} = {new_speed}  // Old Speed: {int(original_speed)}, New Speed: {new_speed}'

# Function to update supply capacity based on the `supply_multiply` flag
def update_supply_capacity(match):
    original_capacity = float(match.group(1))  # Get the original supply capacity as a float
    if supply_multiply:
        new_capacity = int(original_capacity * supply_factor)  # Multiply if the flag is set
    else:
        new_capacity = int(original_capacity / supply_factor)  # Divide otherwise
    # Return the updated line with a comment showing the original and new capacities using //
    return f'{supply_key} = {new_capacity}  // Old Capacity: {int(original_capacity)}, New Capacity: {new_capacity}'

# Function to update fuel capacity based on the `fuel_multiply` flag
def update_fuel_capacity(match):
    original_capacity = float(match.group(1))  # Get the original fuel capacity as a float
    if fuel_multiply:
        new_capacity = int(original_capacity * fuel_factor)  # Multiply if the flag is set
    else:
        new_capacity = int(original_capacity / fuel_factor)  # Divide otherwise
    # Return the updated line with a comment showing the original and new capacities using //
    return f'{fuel_key} = {new_capacity}  // Old Capacity: {int(original_capacity)}, New Capacity: {new_capacity}'

# Regular expressions to find the configurable keys (speed, supply, and fuel)
speed_pattern = re.compile(rf'{speed_key}\s*=\s*(\d+\.?\d*)')
supply_pattern = re.compile(rf'{supply_key}\s*=\s*(\d+\.?\d*)')
fuel_pattern = re.compile(rf'{fuel_key}\s*=\s*(\d+\.?\d*)')

# Replace old speed with the new speed and add the comment
updated_data = re.sub(speed_pattern, update_speed, data)

# Replace old supply capacity with the new capacity and add the comment
updated_data = re.sub(supply_pattern, update_supply_capacity, updated_data)

# Replace old fuel capacity with the new capacity and add the comment
updated_data = re.sub(fuel_pattern, update_fuel_capacity, updated_data)

# Save the updated data to a new file
with open(uniteDescriptor_Modified_path, 'w') as file:
    file.write(updated_data)

print(f"File updated successfully! New file saved at: {uniteDescriptor_Modified_path}")
