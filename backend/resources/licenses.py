import requests

from resources.imports import *
from resources.schemas import *
from core.security.RsaAesDecryption import RsaAesDecrypt
from core.security.RsaAesEncryption import RsaAesEncrypt
from resources.validation_shacl_insert_update import ValidationShaclInsertUpdate


class GetDaliccLicense(MethodResource, Resource):
    @doc(description='Dalicc Licenses', tags=['Dalicc Licenses'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        x = requests.get('https://api.dalicc.net/licenselibrary/list?skip=0&limit=10000')
        # print(result["results"]['bindings'])
        return x.json()

class GetDaliccLicenseById(MethodResource, Resource):
    @doc(description='Dalicc License by Id', tags=['Dalicc Licenses'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, licenseID):
        x = requests.get(f'https://api.dalicc.net/licenselibrary/license/{licenseID}?format=json-ld&download=false')
        return x.json()
