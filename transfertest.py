# connects to the LSM, requests an image, reads it, saves the file.
# Note that the LSM must be connected and properly configured for this code to work.
import sys
import pyvisa
from PIL import Image
from datetime import datetime
    
rm = pyvisa.ResourceManager()

print("Available resources:")
print(rm.list_resources())

print("Opening LSM...")
lsm = rm.open_resource('USB0::1003::8293::GPIB_04_95032313036351211131::0::INSTR')
lsm.timeout = 5000

print("Requesting image...")
lsm.write_raw(b'\xf0\xf5\x71') # enable interface, no dma, request image data
print("Reading...")
total_bytes = 512 * 512
chunk_size = 512
data = b''
bytes_read = 0

while bytes_read < total_bytes:
    chunk = lsm.read_bytes(min(chunk_size, total_bytes - bytes_read))
    data += chunk
    bytes_read += len(chunk)
    progress = (bytes_read / total_bytes) * 100
    print(f"Progress: {progress:.1f}% ({bytes_read}/{total_bytes} bytes)", end='\r')

print()  # New line after progress

print("Done. Closing LSM...")
lsm.write_raw(b'\xf1') # disable interface
lsm.close()

# Convert to PNG
print("Converting to PNG...")
img = Image.frombytes('L', (512, 512), data)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
png_filename = f"lsm_image_{timestamp}.png"
img.save(png_filename)
print(f"Saved PNG as: {png_filename}")