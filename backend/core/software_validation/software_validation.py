import os
from core.query_processor.QueryProcessor import QueryEngine
from core.security.RsaAesEncryption import RsaAesEncrypt


class SoftwareValidation(QueryEngine):

    def __init__(self):
        super().__init__()

    def delete_software(self, softwareID):
        response = self.post_sparql(self.get_username(), self.get_password(),
                                    self.delete_software_by_id(softwareID))
        # delete encryption file from the directory
        cwd = os.getcwd()
        file_name = cwd + '/core/security/bundle' + softwareID + '.enc'
        # remove file from the directory
        os.remove(file_name)
        return response

    def post_data(self, validated_data, type, software_id):
        Name = validated_data["Name"]
        Description = validated_data["Description"]
        CreateDate = validated_data["CreateDate"]
        LicenseId = validated_data["LicenseId"]
        VersionInfo = validated_data["VersionInfo"]

        if Name=="string":
            Name=""

        if Description=="string":
            Description=""

        if LicenseId=="string":
            LicenseId=""

        if VersionInfo=="string":
            VersionInfo=""

        if type == "insert":

            SoftwareId = software_id
            ############## encryption ########################
            data = {'software_id': SoftwareId, 'name': Name, 'description': Description, 'license_id': LicenseId}
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            # print(encrypted_data)

            Name = encrypted_data[1]['name']
            Description = encrypted_data[2]['description']
            LicenseId = encrypted_data[3]['license_id']

            ############## end encryption ########################

            respone = self.post_sparql(self.get_username(), self.get_password(),
                                       self.insert_query_software(SoftwareId=SoftwareId, Name=Name,
                                                                   Description=Description,
                                                                   CreateDate=CreateDate,
                                                                  LicenseId=LicenseId,
                                                                  VersionInfo=VersionInfo))
        else:
            SoftwareId = validated_data["SoftwareId"]
            Description = validated_data["Description"]
            Name = validated_data["Name"]
            LicenseId = validated_data["LicenseId"]
            VersionInfo = validated_data["VersionInfo"]

            ############## encryption ########################
            data = {'software_id': SoftwareId, 'name': Name, 'description': Description, 'license_id': LicenseId}
            obj = RsaAesEncrypt()
            encrypted_data = obj.rsa_aes_encrypt(data)

            Name = encrypted_data[1]['name']
            Description = encrypted_data[2]['description']
            LicenseId = encrypted_data[3]['license_id']


            ############## end encryption ########################
            # print(f"softwareid={SoftwareId}, Name ={Name}, description={Description}, licenseId={LicenseId}")
            if SoftwareId != "":
                # delete from knowledge graph
                response = self.post_sparql(self.get_username(), self.get_password(),
                                            self.delete_software_by_id(SoftwareId))

                # insert into kg
                # print(f"Name ={Name}, description={Description}, licenseId={LicenseId}")
                respone = self.post_sparql(self.get_username(), self.get_password(),
                                           self.insert_query_software(SoftwareId=SoftwareId,
                                                                       Name=Name, Description=Description,
                                                                       CreateDate=CreateDate,
                                                                      LicenseId=LicenseId,
                                                                      VersionInfo=VersionInfo))
        return respone
