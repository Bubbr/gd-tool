import base64
import os
import struct
import sys
import traceback
import zlib
from xml.dom import minidom

__version__ = '1.1.2'

SAVE_FILE_NAME = ['CCGameManager.dat','CCGameManager2.dat', 'CCLocalLevels.dat', 'CCLocalLevels2.dat']
SAVE_FILE_PATH = os.path.join(os.getenv('LocalAppData'), 'GeometryDash')

prettify_xml = True



def xor_bytes(data: bytes, value: int) -> bytes:
    return bytes(map(lambda x: x ^ value, data))

def encrypt():
    for save_file in SAVE_FILE_NAME:
        try:
            print(f'Encrypting {save_file}.xml...')

            with open(f'{save_file}.xml', 'rb') as f:
                decrypted_data = f.read()

            compressed_data = zlib.compress(decrypted_data)
            data_crc32 = zlib.crc32(decrypted_data)
            data_size = len(decrypted_data)

            compressed_data = (b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x0b' +  # gzip header
                                compressed_data[2:-4] +
                                struct.pack('I I', data_crc32, data_size))
            encoded_data = base64.b64encode(compressed_data, altchars=b'-_')
            encrypted_data = xor_bytes(encoded_data, 11)

            with open(os.path.join(SAVE_FILE_PATH, save_file), 'wb') as f:
                f.write(encrypted_data)

            print('Done!')
        except FileNotFoundError as err:
            print(f"Can't find {save_file}.xml in current folder!")
        except Exception as err:
            print(f'Failed to encrypt {save_file}.xml!')
            traceback.print_exc()

def decrypt():
    for save_file in SAVE_FILE_NAME:
        try:
            print(f'Decrypting {save_file}...')

            with open(os.path.join(SAVE_FILE_PATH, save_file), 'rb') as f:
                encrypted_data = f.read()

            decrypted_data = xor_bytes(encrypted_data, 11)
            decoded_data = base64.b64decode(decrypted_data, altchars=b'-_')
            decompressed_data = zlib.decompress(decoded_data[10:], -zlib.MAX_WBITS)

            if prettify_xml:
                try:
                    xml_dom = minidom.parseString(decompressed_data)
                    decompressed_data = xml_dom.toprettyxml(indent='\t', encoding='utf-8')
                except Exception as err:
                    print(f'Failed to prettify {save_file}.xml! File will remain unprettified.')

            with open(f'{save_file}.xml', 'wb') as f:
                f.write(decompressed_data)

            print('Done!')
        except FileNotFoundError as err:
            print(f"Can't find {save_file}.xml in save file folder!")
        except Exception as err:
            print(f'Failed to decrypt {save_file}!')
            traceback.print_exc()
if __name__ == "__main__":
    encrypt()
