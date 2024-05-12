import re

def extract_numerical(text):
    # Use regular expression to find numerical part
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())  # Convert the matched string to an integer
    else:
        return None  # Return None if no numerical part found