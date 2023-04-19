import json
import os


from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class DigitalSignature():
    def digital_signature_verify(self, data):
        # print(data)
        # hexa to byte
        digital_sig_hexa_to_byte = bytes.fromhex(data['signature'])
        message_byte = bytes(data['message'], 'utf-8')
        # print(digital_sig_hexa_to_byte)
        cwd = os.getcwd()
        with open(cwd + '/core/security/private.pem', 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
        try:
            public_key = private_key.public_key()
            public_key.verify(
                digital_sig_hexa_to_byte,
                message_byte,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            # print('Trusted message')
            return 'Trusted message'
        except InvalidSignature:
            # print("Do not trust message")
            return 'Do not trust message'

    def digital_signature(self, data):
        cwd = os.getcwd()
        with open(cwd + '/core/security/private.pem', 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )

        # original_data = str(data["message"] + data["signature"])
        data_in_byte = bytes(data["message"], 'utf-8')
        # print(data_in_byte)
        digial_signature = private_key.sign(
            data_in_byte,
            padding.PSS(mgf=padding.MGF1(
                hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        # print(digial_signature.hex())
        signed_data = {
            'message': data_in_byte,
            'signature': digial_signature.hex()
        }
        # print(json.dumps(signed_data))
        # print(signed_data)
        return signed_data
