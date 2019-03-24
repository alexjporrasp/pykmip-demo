
import binascii
import logging
import sys

from kmip.core import enums
from kmip.demos import utils
from kmip.pie import client


if __name__ == '__main__':
    logger = utils.build_console_logger(logging.INFO)

    # Build and parse arguments
    parser = utils.build_cli_parser(enums.Operation.DECRYPT)
    opts, args = parser.parse_args(sys.argv[1:])
    config = opts.config

    if (len(args) != 1):
        print('Pick a file to decrypt.')
        exit()

    with open(args[0], 'rb') as f:
        f_bytes = f.read()
        uuid = str(int.from_bytes(f_bytes[:20], 'big'))
        enc_file_bytes = f_bytes[20:]

    # Build the client and connect to the server
    with client.ProxyKmipClient(
            config=config,
            config_file=opts.config_file
    ) as client:
        # Decrypt the cipher dara with the encryption key.
        try:
            raw_data = client.decrypt(
                # message,
                enc_file_bytes,
                uid=uuid,
                cryptographic_parameters={
                    'cryptographic_algorithm':
                        enums.CryptographicAlgorithm.AES,
                    'block_cipher_mode': enums.BlockCipherMode.CBC,
                    'padding_method': enums.PaddingMethod.ANSI_X923
                },
                iv_counter_nonce=(
                    b'\x01\x7D\x45\xA0\x88\x08\x11\x11'
                    b'\xF0\x00\x12\xFF\x7A\x3A\x36\x90'
                )
            )

            logger.info("Successfully decrypted the data.")

            with open(''.join(args[0].rsplit('_', 1)[:-1])+'_dec', 'wb+') as f:
                f.write(raw_data)

        except Exception as e:
            logger.error(e)