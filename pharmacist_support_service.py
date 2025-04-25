from flask import Flask, jsonify, request
import grpc
import pharmacist_support_pb2
import pharmacist_support_pb2_grpc

app = Flask(__name__)

# gRPC Client Setup
channel = grpc.insecure_channel('localhost:50052')
stub = pharmacist_support_pb2_grpc.PharmacistSupportStub(channel)

@app.route('/drugs/interactions', methods=['GET'])
def get_drug_interactions():
    drugA = request.args.get('drugA')
    drugB = request.args.get('drugB')
    response = stub.FetchDrugInteractions(pharmacist_support_pb2.DrugPair(drugA=drugA, drugB=drugB))
    return jsonify({"interaction_type": response.interaction_type, "severity": response.severity})

@app.route('/drugs/alternatives', methods=['GET'])
def get_alternative_drugs():
    drug_name = request.args.get('name')
    response = stub.FetchAlternativeDrugs(pharmacist_support_pb2.DrugName(name=drug_name))
    return jsonify([{"name": alt.name, "efficacy_score": alt.efficacy_score} for alt in response.alternatives])

if __name__ == '__main__':
    app.run(port=8081, debug=True)
