from typing import Union, Protocol

class Hex(Protocol):
    def __class_getitem__(cls, _: Union[int, tuple[int, int]]) -> type[int]:
        return int # This tells Pyrigoht: "Treat hex[0xFF] as an int"


class Int(int):
    def __class_getitem__(cls, _: int | tuple[int, int]) -> type[int]:
        """Allows syntax like Int[255] or Int[10, 255]"""
        # In a real tool like Pydantic, you'd return a 
        # specialized type. For basic hints, returning 
        # 'int' ensures compatibility.
        return int



class Connection:
    def __init__(self) -> None:
        pass

    def write(self, *hexes: Hex):
        for hex in hexes:
            pass

conn = Connection()


####################
# Sonderfunktionen #
####################

def set_IEC_mode_on():
    """
    LSM in IEC-Mode schalten
    """
    conn.write(0xF0)

def set_IEC_mode_off():
    """
    IEC-Mode ausschalten (Voreinstellung)
    """
    conn.write(0xF1)

def set_LSM_control_panel_on():
    """
    LSM-Bedienpult einschalten (Voreinstellung)
    """
    conn.write(0xF2)

def set_LSM_control_panel_off():
    """
    LSM-Bedienpult abschalten
    """
    conn.write(0xF3)

def dma_mode_on():
    """
    Die Übertragung vom LSM zum ext. über DMA muß das LSM während der gesamten Übertragungszeit als Talker eingestellt bleiben, andernfalls können Daten verloren gehen
    """
    conn.write(0xF4)

def dma_mode_off():
    """
    (Voreinstellung) Alle Übertragungen laufen wieder über die CPU
    Ausnahme Befehl 0x94 (pc_transfer_from_picture_memory), siehe unten
    """
    conn.write(0xF5)


######################################
# Übertragungs- und Steuerfunctionen #
######################################

def set_contrast(
    value: Int[0, 4095]
):
    high_byte = value >> 8   # shift right 8 bits to get the upper byte
    low_byte = value & 0xFF  # mask to get the lower byte

    conn.write(0xE0, high_byte, low_byte)

def set_brightness(
    value: Int[0, 4095]
):
    high_byte = value >> 8   # shift right 8 bits to get the upper byte
    low_byte = value & 0xFF  # mask to get the lower byte

    conn.write(0xE0, high_byte, low_byte)


def set_zoom(
    x: Int[255],
    y: Int[255]
):
    """
    Zoom für die Koordinaten x und y getrennt einstellen (x,y = 0 ... FF). Bei x = y ist das Seitenverhältnis 3:2 (Normaleinstellung beim LSM, der Zusammenhang von LSM-Zoom-Wert (20 ... 160) und y ergibt sich aus y = 5100/Zoom-Wert. Umschalten auf quadratische Pixel erfogt durch Ändern von entsprechend x = 2/3y; z.b. für Zoom = 20: x=AA, y=FF.
    """
    conn.write(0xE8, x, y)

#TODO: Understand what the documentation means with 750
def move_z(value: Int[32]):
    """
    Schrittweise für z-Antrieb in nm übertragen, Berreich 0...32 750
    """
    high_byte = value >> 8   # shift right 8 bits to get the upper byte
    low_byte = value & 0xFF  # mask to get the lower byte
    conn.write(0xE9, high_byte, low_byte)

def set_rotation_angle(value: Int[4095]):
    """
    Rotations-Winkel einstellen (phi-z-Scan, Rotate Frame)
    """
    high_byte = value >> 8   # shift right 8 bits to get the upper byte
    low_byte = value & 0xFF  # mask to get the lower byte
    conn.write(0xEA, high_byte, low_byte)

def set_line_position(value: Int[4095]):
    """
    Linienposition einstellen (phi-z-Scan)
    """
    high_byte = value >> 8   # shift right 8 bits to get the upper byte
    low_byte = value & 0xFF  # mask to get the lower byte
    conn.write(0xEA, high_byte, low_byte)

def image_scan_512():
    """
    Bild 512x512 scannen
    """
    conn.write(0x88)

def image_pc_scan_512():
    """
    Bild 512x512 im LSM-Bildspeicher zum externen Rechner senden (512x512 Byte)
    """
    conn.write(0x71)

def image_scan_256_linear_to_memory():
    """
    Bild 256x256 scannen und linear in den LSM-Bildspeicher schreiben
    """
    conn.write(0x92)

def send_image_256_linear_to_pc():
    """
    Bild 256x256 linear zum ext. Rechner senden (256x256 Byte)
    """
    conn.write(0x93)

def recv_image_512_from_pc():
    """
    Bild 512x512 vom externen Rechner zum LSM-Bildspeicher übertragen
    """
    conn.write(0x70)

def image_scan_512_synced_to_pc():
    """
    Bold 512x512 scannen und synchron zum externen Rechner senden
    """
    conn.write(0x72)






def pc_transfer_from_picture_memory(
        pic_mem_address: Int[255], # in kByte
        block_length: Int[1, 64], # in kByte
        period: Int[0] | Int[35, 255], # in 100ns steps
    ):
    """
    Datenblock vom LSM-Bildspeicher über DMA zum externen Rechner übetragen
        pic_mem_address (a): Bildspeicheradresse in kByte-Schritten 0...255
        block_length (b): Blocklänge in kByte 1...64
        period (c): Periodendauer in 100ns-Schritten 35...255
            c=0: DMA-Übertragung Handshake gesteuert, max. Geschwindigkeit
            c>0: DMA-Übertragung mit festem Übertragungstakt
    """
    conn.write(0x94, pic_mem_address, block_length, period)
