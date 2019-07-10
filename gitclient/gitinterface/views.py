from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from rest_framework.parsers import FileUploadParser

from rest_framework.views import APIView
from rest_framework.response import Response

import grpc
import git_pb2
import git_pb2_grpc


import tempfile

# Create your views here.

class GRPCInitView(APIView):
    def get(self, request, format=None):
        channel = grpc.insecure_channel('localhost:50051')
        stub = git_pb2_grpc.GitStub(channel)
        response = stub.CreateAndInitDirectory(git_pb2.Request_Path(path="nexivil6/hosuk6"))
        responsee = { 'result':response.result}        
        #print(response)                                
        return Response(responsee)


class GRPCAddView(APIView):
    def get(self, request, format=None):
        channel = grpc.insecure_channel('localhost:50051')
        stub = git_pb2_grpc.GitStub(channel)
        f = open('./gittest.txt', "rb")
        filedata = f.read()
        response = stub.AddOrUpdateFile(git_pb2.Request_File(path="nexivil6/hosuk6", filedata= filedata, filename="gittest.txt", filemode=100664))
        f.close()
        responsee = { 'result':response.result}        
        #print(response)                                
        return Response(responsee)



class zzzFileUploadViewzzz(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request ,format=None):
        file_obj = request.FILES['file']
        channel = grpc.insecure_channel('localhost:50051')
        stub = git_pb2_grpc.GitStub(channel)
        filename = file_obj._get_name()
        filedata = file_obj.file.read()
        response = stub.AddOrUpdateFile(git_pb2.Request_File(path="nexivil6/hosuk6", filedata=filedata, filename=filename, filemode=100664))
        responsee = { 'result':response.result}
        return Response(responsee)