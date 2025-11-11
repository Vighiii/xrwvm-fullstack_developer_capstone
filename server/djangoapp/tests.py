# Import the function to be tested
from restapis import get_request  # Replace `your_module_name` with the actual module name

# Test the get_request function
response = get_request("/api/example", param1="value1", param2="value2")
if response:
    print(response)
else:
    print("Failed to get a valid response.")