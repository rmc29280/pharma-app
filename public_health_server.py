import grpc
from concurrent import futures
import public_health_pb2
import public_health_pb2_grpc

class PublicHealthService(public_health_pb2_grpc.PublicHealthServicer):
    def FetchAdverseEvents(self, request, context):
        adverse_events = [
            public_health_pb2.AdverseEvent(substance_name="Paracetamol", reaction="Skin Rash"),
            public_health_pb2.AdverseEvent(substance_name="Ibuprofen", reaction="Nausea")
        ]
        return public_health_pb2.AdverseEventsResponse(events=adverse_events)

    def FetchVaccineReactions(self, request, context):
        reactions = [
            public_health_pb2.VaccineReaction(vaccine_name="Influenza Vaccine", symptoms="Mild Fever"),
            public_health_pb2.VaccineReaction(vaccine_name="COVID-19 Vaccine", symptoms="Fatigue")
        ]
        return public_health_pb2.VaccineReactionsResponse(reactions=reactions)

    def FetchPrescriptionStats(self, request, context):
        stats = [
            public_health_pb2.PrescriptionStats(drug_name="Amoxicillin", total_prescribed=1500),
            public_health_pb2.PrescriptionStats(drug_name="Metformin", total_prescribed=2000)
        ]
        return public_health_pb2.PrescriptionStatsResponse(stats=stats)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    public_health_pb2_grpc.add_PublicHealthServicer_to_server(PublicHealthService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Public Health Monitoring gRPC Server Running on Port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()