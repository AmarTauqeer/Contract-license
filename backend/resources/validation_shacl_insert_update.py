import textwrap

import rootpath
from pyshacl import validate
from rdflib import Graph
from flask_apispec import MethodResource
from flask_restful import Resource

# get shacl shapes
main_directory = f"{rootpath.detect()}/resources/data-graphs-files"
file_name = '/shacl_shapes_insert_update.ttl'
complete_path = main_directory + file_name
file = open(complete_path, 'r')
content = file.read()
shapes = content
file.close()
shacl_file = shapes


# print(shacl_file)

def prefix():
    prefix = textwrap.dedent("""@prefix base: <http://ontologies.atb-bremen.de/smashHitCore#> .
            @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
            @prefix schema: <http://schema.org/> .
            @prefix dct: <http://purl.org/dc/terms/> .
            @prefix fibo-fnd-agr-ctr: <https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/> .
            @prefix prov: <http://www.w3.org/ns/prov#> .
            @prefix time: <http://www.w3.org/2006/time#> .
            @prefix dc: <http://purl.org/dc/elements/1.1/> .
            @prefix sh: <http://www.w3.org/ns/shacl#> .
            @prefix ex: <http://example.com/ns#> .
            @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    """)
    return prefix


class ValidationShaclInsertUpdate(MethodResource, Resource):

    def validation_shacl_insert_update(self, case=None, name=None, contid=None, typeid=None, termid=None, oblid=None,
                                       contractorid=None, compid=None, contstatus=None, contcategory=None,
                                       conttype=None, oblstate=None, consstate=None, purpose=None, enddate=None,
                                       exedate=None, effecdate=None, desc=None, createdate=None, fulfillmentdate=None,
                                       consValue=None, country=None, role=None, email=None, address=None, phone=None,
                                       territory=None, vat=None, softwareid=None, licenseid=None, version=None):
        if case == "termtypes":
            data_graph = """
                            {0}
                            base:{1} a base:TermTypes;
                            base:hasName "{2}";
                            dct:description "{3}" .
                            """.format(prefix(), typeid, name, desc)

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'term_types_violoations': message
            }
            return violation_data
        elif case == "software":
            data_graph = """
                            {0}
                            base:{1} a dc:Software;
                            base:hasName "{2}";
                            dct:description "{3}";
                            base:licenseID "{4}";
                            dc:hasVersion "{5}".
                            """.format(prefix(), softwareid, name, desc, licenseid, version)

            # print(data_graph)
            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'software_violoations': message
            }
            return violation_data
        elif case == "term":
            data_graph = """
                            {0}
                            base:{1} a base:TermsAndConditions;
                            base:hasCreationDate "{2}"^^xsd:dateTime;
                            dct:description "{3}" .
                            """.format(prefix(), termid, createdate, desc)

            print(f"data graph={data_graph}")

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'term_violoations': message
            }
            return violation_data

        elif case == "obligation":
            data_graph = """
                            {0}
                            base:{1} a base:Obligation;
                            base:hasEndDate "{2}"^^xsd:dateTime;
                            fibo-fnd-agr-ctr:hasExecutionDate "{3}"^^xsd:dateTime;
                            base:fulfillmentDate "{4}"^^xsd:dateTime;
                            base:contractorID "{5}";
                            dct:description "{6}";
                            base:hasStates base:{7} .
                            """.format(prefix(), oblid, enddate, exedate, fulfillmentdate, contractorid, desc, oblstate)

            # print(f"data graph={data_graph}")

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'obligation_violoations': message
            }
            return violation_data

        elif case == "contract":
            data_graph = """
                            {0}
                            base:{1} a fibo-fnd-agr-ctr:Contract;
                            base:hasEndDate "{2}"^^xsd:dateTime;
                            fibo-fnd-agr-ctr:hasExecutionDate "{3}"^^xsd:dateTime;
                            fibo-fnd-agr-ctr:hasEffectiveDate "{4}"^^xsd:dateTime;
                            base:forPurpose "{5}";
                            base:hasContractStatus base:{6};
                            base:contractType base:{7};
                            base:hasContractCategory base:{8};
                            rdf:value {9} .
                            """.format(prefix(), contid, enddate, exedate, effecdate, purpose, contstatus, conttype,
                                       contcategory, consValue)

            # print(f"data graph={data_graph}")

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'contract_violoations': message
            }
            return violation_data

        elif case == "contractor":
            data_graph = """
                            {0}
                            base:{1} a prov:Agent;
                            base:hasCompany "{2}";
                            base:hasName "{3}";
                            base:hasEmail "{4}";
                            base:hasTelephone "{5}";
                            base:hasPostalAddress "{6}";
                            base:hasTerritory "{7}";
                            base:hasRole base:{8};
                            base:hasVATIN "{9}";
                            base:hasCreationDate "{10}"^^xsd:dateTime;
                            base:hasCountry "{11}" .
                            """.format(prefix(), contractorid, compid, name, email, phone, address, territory, role,
                                       vat, createdate, country)

            # print(f"data graph={data_graph}")

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'contractor_violoations': message
            }
            return violation_data

        elif case == "company":
            data_graph = """
                            {0}
                            base:{1} a prov:Organization;
                            base:hasName "{2}";
                            base:hasEmail "{3}";
                            base:hasTelephone "{4}";
                            base:hasPostalAddress "{5}";
                            base:hasTerritory "{6}";
                            base:hasVATIN "{7}";
                            base:hasCreationDate "{8}"^^xsd:dateTime;
                            base:hasCountry "{9}" .
                            """.format(prefix(), compid, name, email, phone, address, territory, vat, createdate,
                                       country)

            # print(f"data graph={data_graph}")

            d = Graph().parse(data=data_graph, format="turtle")
            s = Graph().parse(data=shacl_file, format="turtle")
            conforms, report, message = validate(d, shacl_graph=s, advanced=True, debug=False)
            violation_data = {
                'company_violoations': message
            }
            return violation_data
