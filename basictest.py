# connects to the LSM, requests an image, reads it, and prints it as greyscale in the terminal. 
# It also saves the raw image data to a file named "image.bin". Note that the LSM must be connected
# and properly configured for this code to work.
import sys
import pyvisa

def print_greyscale(data: bytes, width: int = 512, height: int = 512):
    """
    Renders a greyscale byte array to the terminal using ANSI true-color
    background escape codes. Each pixel is one space character.
    """
    assert len(data) == width * height, \
        f"Expected {width * height} bytes, got {len(data)}"

    reset = "\033[0m"
    rows = []
    for y in range(height):
        parts = []
        for x in range(width):
            v = data[y * width + x]
            parts.append(f"\033[48;2;{v};{v};{v}m ")
        rows.append("".join(parts) + reset)

    sys.stdout.write("\n".join(rows) + "\n")
    
rm = pyvisa.ResourceManager()
# rm.list_resources()
print("Opening LSM...")
lsm = rm.open_resource('USB0::1003::8293::GPIB_04_95032313036351211131::0::INSTR')
lsm.timeout = 2000
#lsm.write_raw(b'\xf0\x8a') # clear screen

print("Requesting image")
lsm.write_raw(b'\xf0\xf5\x71') # enable interface, no dma, request image data
print("Reading...")
data = lsm.read_bytes(512*512,512) # read image data in 512 byte chunks (chunksize cant be too large or it wont work)
print("Done. Closing LSM...")
lsm.write_raw(b'\xf1') # disable interface

lsm.close()

print(data)

print_greyscale(data)

with open("image.bin", "wb") as filed:
    filed.write(data)
    
