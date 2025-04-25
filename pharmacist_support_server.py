import grpc
from concurrent import futures
import pharmacist_support_pb2
import pharmacist_support_pb2_grpc

class PharmacistSupportService(pharmacist_support_pb2_grpc.PharmacistSupportServicer):
    def FetchDrugInteractions(self, request, context):
        if request.drugA == "Aspirin" and request.drugB == "Warfarin":
            return pharmacist_support_pb2.DrugInteractionResponse(interaction_type="Antagonistic", severity="Severe")
        return pharmacist_support_pb2.DrugInteractionResponse(interaction_type="None", severity="Low")

    def FetchAlternativeDrugs(self, request, context):
        alternatives = [
            pharmacist_support_pb2.AlternativeDrug(name="Naproxen", efficacy_score=8.5),
            pharmacist_support_pb2.AlternativeDrug(name="Celecoxib", efficacy_score=7.8)
        ]
        return pharmacist_support_pb2.AlternativeDrugsResponse(alternatives=alternatives)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pharmacist_support_pb2_grpc.add_PharmacistSupportServicer_to_server(PharmacistSupportService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Pharmacist Support gRPC Server Running on Port 50052...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()