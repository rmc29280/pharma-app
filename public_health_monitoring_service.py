from flask import Blueprint, jsonify, request
import grpc
import os
from flask_jwt_extended import jwt_required
from error_handler import APIError
import public_health_pb2
import public_health_pb2_grpc

# Create blueprint for public health monitoring
public_health_bp = Blueprint('public_health', __name__)

# gRPC Client Setup
def get_grpc_stub():
    channel = grpc.insecure_channel(f"{os.getenv('PUBLIC_HEALTH_GRPC_HOST', 'localhost')}:{os.getenv('PUBLIC_HEALTH_GRPC_PORT', '50051')}")
    return public_health_pb2_grpc.PublicHealthStub(channel)

@public_health_bp.route('/adverse-events', methods=['GET'])
@jwt_required()
def get_adverse_events():
    try:
        stub = get_grpc_stub()
        response = stub.FetchAdverseEvents(public_health_pb2.Empty())
        return jsonify([{"substance_name": event.substance_name, "reaction": event.reaction} for event in response.events])
    except grpc.RpcError as e:
        raise APIError(f"gRPC service error: {e.details()}", status_code=500)

@public_health_bp.route('/vaccines/reactions', methods=['GET'])
@jwt_required()
def get_vaccine_reactions():
    try:
        stub = get_grpc_stub()
        response = stub.FetchVaccineReactions(public_health_pb2.Empty())
        return jsonify([{"vaccine_name": reaction.vaccine_name, "symptoms": reaction.symptoms} for reaction in response.reactions])
    except grpc.RpcError as e:
        raise APIError(f"gRPC service error: {e.details()}", status_code=500)

@public_health_bp.route('/prescriptions/stats', methods=['GET'])
@jwt_required()
def get_prescription_stats():
    try:
        stub = get_grpc_stub()
        response = stub.FetchPrescriptionStats(public_health_pb2.Empty())
        return jsonify([{"drug_name": stat.drug_name, "total_prescribed": stat.total_prescribed} for stat in response.stats])
    except grpc.RpcError as e:
        raise APIError(f"gRPC service error: {e.details()}", status_code=500)
