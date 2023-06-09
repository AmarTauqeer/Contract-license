import json
import os

from core.query_processor.QueryProcessor import QueryEngine
from core.security.RsaAesEncryption import RsaAesEncrypt
from core.security.DigitalSignature import DigitalSignature


class ContractSignatureValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_contract_signature(self, signaureID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_contract_signature_by_id(signaureID))
        # delete encryption file from the directory
        cwd = os.getcwd()
        file_name = cwd + '/core/security/bundle' + signaureID + '.enc'
        # remove file from the directory
        os.remove(file_name)
        return response

    def post_data(self, validated_data, type, signature_id):
        ContractorId = validated_data["ContractorId"]
        CreateDate = validated_data["CreateDate"]
        Signature = validated_data["Signature"]

        if type == "insert":
            SignatureId = signature_id

            ############## digital signature ########################
            signature_data = {'message': ContractorId}
            obj_sig = DigitalSignature()
            data_from_signature = obj_sig.digital_signature(signature_data)
            digital_signature=data_from_signature["signature"]
            ############## end digital signature ########################

            ############## encryption ########################
            data = {'signature_id': SignatureId, 'signature': Signature}
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Signature = encrypted_data[1]['signature']
            ############## end encryption ########################
            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_contract_signature(SignatureId=SignatureId,
                                                                            ContractorId=ContractorId,
                                                                            CreateDate=CreateDate,
                                                                            Signature=Signature,
                                                                            DigitalSignature=digital_signature,
                                                                            )

                                       )
        else:
            SignatureId = validated_data["SignatureId"]
            ############## digital signature ########################
            sngnature_data = {'message': ContractorId}
            obj_sig = DigitalSignature()
            data_from_signature = obj_sig.digital_signature(sngnature_data)
            digital_signature = data_from_signature["signature"]
            ############## end signature ########################

            ############## encryption ########################
            data = {'signature_id': SignatureId, 'signature': Signature}
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Signature = encrypted_data[1]['signature']
            ############## end encryption ########################

            if SignatureId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_contract_signature_by_id(SignatureId))

                # insert into kg
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_contract_signature(SignatureId=SignatureId,
                                                                                ContractorId=ContractorId,
                                                                                CreateDate=CreateDate,
                                                                                Signature=Signature,
                                                                                DigitalSignature=digital_signature,
                                                                                )

                                           )
        return respone
