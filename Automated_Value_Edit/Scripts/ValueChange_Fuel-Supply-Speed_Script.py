import re
import os

# File paths for the vehicle data
file_path = r"C:\Users\SgtDevRupesh_MW\Downloads\vehicle_data.txt"
output_file_path = r"C:\Users\SgtDevRupesh_MW\Downloads\updated_vehicle_data.txt"

# Configurable variables
speed_division_factor = 1.25  # Factor to divide MaxSpeedInKmph
supply_multiplication_factor = 2  # Factor to multiply SupplyCapacity
fuel_multiplication_factor = 2  # Factor to multiply FuelCapacity

# Open the file containing the vehicle data
with open(file_path, 'r') as file:
    data = file.read()

# Function to update speed and ensure the result is a whole number
def update_speed(match):
    original_speed = float(match.group(1))  # Get the original speed as a float
    new_speed = int(original_speed / speed_division_factor)  # Divide by the configurable factor
    # Return the updated line with a comment showing the original and new speeds using //
    return f'MaxSpeedInKmph = {new_speed}  // Old Speed: {int(original_speed)}, New Speed: {new_speed}'

# Function to update supply capacity
def update_supply_capacity(match):
    original_capacity = float(match.group(1))  # Get the original supply capacity as a float
    new_capacity = int(original_capacity * supply_multiplication_factor)  # Multiply by the configurable factor
    # Return the updated line with a comment showing the original and new capacities using //
    return f'SupplyCapacity = {new_capacity}  // Old Capacity: {int(original_capacity)}, New Capacity: {new_capacity}'

# Function to update fuel capacity
def update_fuel_capacity(match):
    original_capacity = float(match.group(1))  # Get the original fuel capacity as a float
    new_capacity = int(original_capacity * fuel_multiplication_factor)  # Multiply by the configurable factor
    # Return the updated line with a comment showing the original and new capacities using //
    return f'FuelCapacity = {new_capacity}  // Old Capacity: {int(original_capacity)}, New Capacity: {new_capacity}'

# Regular expressions to find MaxSpeedInKmph, SupplyCapacity, and FuelCapacity values
speed_pattern = re.compile(r'MaxSpeedInKmph\s*=\s*(\d+\.?\d*)')
supply_pattern = re.compile(r'SupplyCapacity\s*=\s*(\d+\.?\d*)')
fuel_pattern = re.compile(r'FuelCapacity\s*=\s*(\d+\.?\d*)')

# Replace old speed with the new speed and add the comment
updated_data = re.sub(speed_pattern, update_speed, data)

# Replace old supply capacity with the new capacity and add the comment
updated_data = re.sub(supply_pattern, update_supply_capacity, updated_data)

# Replace old fuel capacity with the new capacity and add the comment
updated_data = re.sub(fuel_pattern, update_fuel_capacity, updated_data)

# Save the updated data to a new file
with open(output_file_path, 'w') as file:
    file.write(updated_data)

print(f"File updated successfully! New file saved at: {output_file_path}")