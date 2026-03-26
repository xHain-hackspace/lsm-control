"""
Mit dieser Zusatzsoftware (480088-9902) wird eine komfortable
Kopplung des LSM mit einem externen Rechnersystem möglich.
Sie gestattet die Fernsteuerbarkeit des LSM in allen Funktionen
und bietet verschiedene Zusatzfunktionen, die sonst nicht zur
Verfügung stehen (z.B. Feinpositionierung der Scanner, Arbeiten
mit Fenstern (area of interest = AOI) ).
Diese Zusatzsoftware umfaßt folgenden Befehlsvorrat enschließ-
lich der in der Grundsoftware enthaltenen Befehle:

¹⁾ Wertebereich 0 ... 4095
    Umrechnung vom Display-Wert (0 ... 999):
    Eingabewert nn = (4095/999)*Displaywert

²⁾ Feinpositionierung ist möglich (Bereich 0x0 ... 0x0FFF).
    Soll eine Spalte aus dem fertig beschrieben Bildspeicher
    angesprochen werden (Speicherspalten 1 ... 512), ist die
    Position einzugeben entsprechend der Beziehung
    X-Position nn = (Speicherspalten - 1)x7.1
   Beispiel:
    Zum Ansprechen der 15. Speicherspalte ist
    nn(dezimal) = 99.4, nn(hex) = 0x0063
   Voreinstellung:
    0x0800.
   Bemerkung:
    Aus technischen Gründen ist die genaue Position von der
    Geschwindigkeit des Scanners abhängig. Mit zunehmender
    Scangeschwindigkeit tritt ein wachsender x-Offset-Wert auf.

³⁾ Feinpositionierung ist möglich (Bereich 0x0 ... 0x0FFF).
    Soll eine Spalte aus dem fertig beschrieben Bildspeicher
    angesprochen werden (Speicherspalten 1 ... 512), ist die
    Position einzugeben entsprechend der Beziehung
    Y-Position nn = (Speicherspalten - 1)x8
   Beispiel:
    15. Speicherzeile ist nn(dezimal) = 112 bzw. nn(hex) = 0x0070
   Voreinstellung:
    0x0800.
   Bemerkung:
    Wegen deutlich kleineren Geschwindigkeit des y-
    Scanners tritt hier bei ²⁾ angesprochene Scanoffset nicht in
    Erscheinung

⁴⁾ Feinpositionierung ist möglich (Bereich 0 ... 0x0E00)
    X-Position nn = (Speicherspalte -1)x8;
    Speicherspalte = 1 ... 449
   Voreinstellung:
    0x0700.


⁵⁾ Feinpositionierung ist möglich (Bereich 0 ... 0x0E00)
    Y-Position nn = (Speicherspalte -1)x8;
    Speicherspalte = 1 ... 449
   Voreinstellung:
    0x0700.

⁶⁾ LSM-Status: 20 Byte werden gesendet
    1.  Byte: Kennung 0xA6
    2.  Byte: Funktion
         0 = Frame
         1 = Linie
         2 = Spot
         3 = _
         4 = Overlay
         5 = Averaging
         6 = Standby
         7 = -
         8 = Fastscan
    3.  Byte:
         0 = Live
         1 = Store
    4.  Byte: Betriebsart
         1 = Konvent. Auflicht # TODO: Für was steht Konvent.
         2 = Konvent. Durchlicht
         3 = Floureszenz
         4 = LSM Auflicht
         5 = LSM Durchlicht
         6 = OBIC # TODO: Für was steht OBIC
    5.  Byte: Tastaturstatus
         5  = Zoom
         6  = Lens
         7  = Filter
         26 = X
         28 = F
    6.  Byte: Laser (z. Zt. nur Laser1/Laser2)
    7.  Byte: tscan
         0 = 2 sec
         1 = 8 sec
    8.  Byte: Confoc.
         0 = off
         1 = on
    9.  Byte: Color
         0 = off
         1 = on
    10. Byte: TV
         0 = off
         1 = on
    11. Byte: Contrast rücklesen
         (höherwertiges Byte)
    12. Byte: Contrast rücklesen
         (niederwertiges Byte)
    13. Byte: Brightness rücklesen
         (höherwertiges Byte)
    14. Byte: Brightness rücklesen
         (niederwertiges Byte)
    15. Byte: Zoomwert
         (20 - 160)
    16. Filterstellung
         (0 - 3 bzw. 0 - 4)
    17. Byte: Revolverposition
         (1...5)
    18. Byte: Optionen
         76543210
         XXZSMMMM

         0M & 1M:
             0b01: 2 MIPs 
             0b00: 1 MIP
         2M:
             0b1: Master MIP 1024
             0b0: Master MIP 512
         3M:
             0b1: Master MIP 1024
             0b0: Master MIP 512
         4S: SCSI-Schnittstelle:
             0b1: vorhanden
             0b0: nicht vorhanden
         5Z: z-Motor:
             0b1: vorhanden
             0b0: nicht vorhanden
    19. Byte: Reserve
    20. Byte: Reserve
"""

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



def transfer_line(linenumber):
    """
    Zeilennummer übertragen ³⁾
    """
    high_byte = linenumber >> 8   # shift right 8 bits to get the upper byte
    low_byte = linenumber & 0xFF  # mask to get the lower byte
    conn.write(0xE2, high_byte, low_byte)

def line_scan_to_picture_memory():
    """
    Zeile scannen und in den Bildspeicher übertragen
    (sichtbar).
    """
    conn.write(0x73)

def line_scan_to_interface_memory():
    """
    Zeile scannen und in das Interface-RAM übertragen
    (unsichtbar).
    """
    conn.write(0x74)

def line_interface_memory_to_pc():
    """
    Zeile im Interface-RAM zum ext. Rechner senden
    (512 Byte).
    """
    conn.write(0x78)

def line_picture_memory_to_pc():
    """
    Zeile im LSM-Bildspeicher zum ext. Rechner senden
    (512 Byte).
    """
    conn.write(0x77)

def line_pc_to_picture_memory():
    """
    Zeile vom ext. Rechner zum LSM-Bildspeicher
    übertragen.
    """
    conn.write(0x75)

def scan_line_synced_to_pc():
    """
    Zeile scannen und synchron zum ext. Rechner senden.
    """
    conn.write(0x75)



def set_AOI_position_x(value):
    """
    AOI-Position x ⁴⁾
    """
    high_byte = value >> 8   # shift right 8 bits to get the upper byte
    low_byte = value & 0xFF  # mask to get the lower byte
    conn.write(0xE4, high_byte, low_byte)

def set_AOI_position_y(value):
    """
    AOI-Position y ⁵⁾
    """
    high_byte = value >> 8   # shift right 8 bits to get the upper byte
    low_byte = value & 0xFF  # mask to get the lower byte
    conn.write(0xE5, high_byte, low_byte)

def scan_AOI_to_interface_memory():
    """
    AOI scannen und in das Interface-RAM übetragen
    """
    conn.write(0x7A)

def AOI_interface_memory_to_pc():
    """
    AOI im Interface-RAM zum externen Rechner senden
    (64x64 Byte)
    """
    conn.write(0x7B)

def scan_AOI_to_picture_memory():
    """
    AOI scannen und in den Bildspeicher übetragen
    (für Testzwecke)
    """
    conn.write(0x90)

def AOI_pc_to_picture_memory():
    """
    AOI vom externen Rechner zum LSM-Bildspeicher übetragen
    (für Testzwecke)
    """
    conn.write(0x91)

def scan_AOI_synced_to_pc():
    """
    AOI scannen und synchron zum externen Rechner senden
    """
    conn.write(0x79)




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


