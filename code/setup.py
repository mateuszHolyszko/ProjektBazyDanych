import nltk
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install required packages
install("numpy")
install("nltk")

# Download NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

print("Setup complete. All necessary packages and NLTK data have been installed.")
