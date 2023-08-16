import requests

from resources.imports import *
from resources.schemas import *
from core.security.RsaAesDecryption import RsaAesDecrypt
from core.security.RsaAesEncryption import RsaAesEncrypt
from resources.validation_shacl_insert_update import ValidationShaclInsertUpdate


class GetSoftwareLicense(MethodResource, Resource):
    @doc(description='Software Licenses', tags=['Software Licenses'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="softwareLicenses", termID=None,
                                   contractRequester=None, contractProvider=None, ))
        response = response["results"]['bindings']

        if len(response) != 0:
            obj_dec = RsaAesDecrypt()
            term_array = []
            for r in response:
                data = {'software_id': r['softwareId']['value'], 'name': r['name']['value'],
                        'description': r['description']['value'],'license_id': r['licenseId']['value']}
                decrypted_result = obj_dec.rsa_aes_decrypt(data)
                # print(decrypted_result)
                name = decrypted_result[0]['name']
                description = decrypted_result[1]['description']
                license_id = decrypted_result[2]['license_id']
                data = {
                    'softwareId': r['softwareId']['value'],
                    'name': name,  # r['name']['value'],
                    'description': description,  # r['description']['value'],
                    'licenseId':license_id,
                    'hasVersion':r['versionInfo']['value'],
                    'createDate': r['createDate']['value'],
                }
                term_array.append(data)
            return term_array
        return 'No record found for this ID'


class SoftwareById(MethodResource, Resource):
    @doc(description='Software Licenses', tags=['Software Licenses'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    def get(self, softwareID):
        query = QueryEngine()
        response = json.loads(
            query.select_query_gdb(purpose=None, dataRequester=None, additionalData="softwareID", softwareID=softwareID,
                                   contractRequester=None, contractProvider=None, termID=None))
        res = response["results"]['bindings']
        if len(res) > 0:
            res = res[0]
            obj_dec = RsaAesDecrypt()
            data = {'software_id': res['softwareId']['value'], 'name': res['name']['value'],
                    'description': res['description']['value'], 'license_id': res['licenseId']['value']}
            decrypted_result = obj_dec.rsa_aes_decrypt(data)
            name = decrypted_result[0]['name']
            description = decrypted_result[1]['description']
            license_id = decrypted_result[2]['license_id']
            data = {
                'softwareId': res['softwareId']['value'],
                'name': name,  # r['name']['value'],
                'description': description,  # r['description']['value'],
                'licenseId': license_id,
                'hasVersion': res['versionInfo']['value'],
                'createDate': res['createDate']['value'],
            }
            return data
        return "No record available for this term type id"


class SoftwareDeleteById(MethodResource, Resource):
    @doc(description='Software Licenses', tags=['Software Licenses'])
    # @check_for_session
    # @Credentials.check_for_token
    # @marshal_with(BulkResponseQuerySchema)
    # @use_kwargs(ContractRequestSchema)
    def delete(self, softwareID):
        # get contract status from db
        result = SoftwareById.get(self, softwareID)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)

        if decoded_data != 'No record available for this software id':
            if decoded_data['softwareId'] == softwareID:
                av = SoftwareValidation()
                response = av.delete_software(softwareID)
                if (response):
                    return jsonify({'Success': "Record deleted successfully."})
                else:
                    return jsonify({'Error': "Record not deleted due to some errors."})
            return jsonify({'Success': "Record doesn't matched."})
        return jsonify({'Success': "Record doesn't exist."})


class SoftwareCreate(MethodResource, Resource):
    @doc(description='Software Licenses', tags=['Software Licenses'])
    # @check_for_session
    # @Credentials.check_for_token
    @use_kwargs(SoftwareRequestSchema)
    def post(self, **kwargs):
        schema_serializer = SoftwareRequestSchema()
        data = request.get_json(force=True)
        # print(data)
        uuidOne = uuid.uuid1()
        software_id = "software_" + str(uuidOne)
        validation_result = ValidationShaclInsertUpdate.validation_shacl_insert_update(self, case="software", softwareid=software_id, name=data['Name'],
                                                        desc=data['Description'], licenseid=data['LicenseId'], version=data['VersionInfo'])
        if 'sh:Violation' in validation_result['software_violoations']:
            return  validation_result['software_violoations']

        # # shacl validation
        # validation_data= [{
        #         'validation':'termtypes',
        #         'typeId':term_type_id,
        #         'name': data['Name'],
        #         'description': data['Description'],
        #     }]
        #
        # print(f"validation data= {validation_data}")
        # # send data to validator and receive result
        # validator_url = "http://localhost:8080/RestDemo/validation"
        # # validator_url = "http://138.232.18.138:8080/RestDemo/validation"
        # r = requests.post(validator_url, json=validation_data)
        # validation_result = r.text
        # # print(validation_result)
        #
        # if validation_result!="":
        #     return  validation_result

        # if validation_result!="":
        #     validation_result_data={}
        #     if "hasName" in validation_result:
        #         validation_result_data['hasName']='check name field'
        #     if 'description' in validation_result:
        #         validation_result_data['description']='check description field'
        #     return validation_result_data

        validated_data = schema_serializer.load(data)
        av = SoftwareValidation()
        response = av.post_data(validated_data, type="insert", software_id=software_id)
        if response == 'Success':
            contract_obj = SoftwareById.get(self, software_id)
            contract_obj = contract_obj.json
            return contract_obj
        else:
            return jsonify({'Error': "Record not inserted due to some errors."})


class SoftwareUpdate(MethodResource, Resource):
    @doc(description='Software Licenses', tags=['Software Licenses'])
    # @check_for_session
    # @Credentials.check_for_token
    @marshal_with(BulkResponseQuerySchema)
    @use_kwargs(SoftwareUpdateSchema)
    def put(self, **kwargs):
        schema_serializer = SoftwareUpdateSchema()
        data = request.get_json(force=True)
        # print(data)
        software_id = data['SoftwareId']
        # get contract status from db
        result = SoftwareById.get(self, software_id)
        my_json = result.data.decode('utf8')
        decoded_data = json.loads(my_json)
        # print(decoded_data)
        if decoded_data != 'No record available for this software id':
            if decoded_data['softwareId'] == software_id:

                validation_result = ValidationShaclInsertUpdate.validation_shacl_insert_update(self, case="software",
                                                                                               softwareid=software_id,
                                                                                               name=decoded_data['name'],
                                                                                               desc=decoded_data['description'],
                                                                                               version=decoded_data['versionInfo'])
                if 'sh:Violation' in validation_result['software_violoations']:
                    return validation_result['software_violoations']

                validated_data = schema_serializer.load(data)
                av = SoftwareValidation()
                response = av.post_data(validated_data, type="update", software_id=None)
                if (response):
                    return jsonify({'Success': "Record updated successfully."})
                else:
                    return jsonify({'Error': "Record not updated due to some errors."})
            else:
                return jsonify({'Error': "Record doesn't exist ."})
        return jsonify({'Error': "Record doesn't exist ."})
