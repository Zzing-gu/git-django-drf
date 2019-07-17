from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from rest_framework.parsers import FileUploadParser

from rest_framework.views import APIView
from rest_framework.response import Response

from gitinterface.serializers import TreeSerializer

from rest_framework.renderers import JSONRenderer



from google.protobuf.json_format import MessageToJson , MessageToDict



import grpc
import git_pb2
import git_pb2_grpc

import re

import json


# Create your views here.

class GRPCInitView(APIView):
    def post(self, request, format=None):
        path = request.data['path']
        channel = grpc.insecure_channel('localhost:50051')
        stub = git_pb2_grpc.GitStub(channel)
        response = stub.CreateAndInitDirectory(git_pb2.Request_Path(path=path))
        responsee = { 'result':response.result}        
        #print(response)                                
        return Response(responsee)


class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request ,format=None):
        file_obj = request.FILES['file']
        channel = grpc.insecure_channel('localhost:50051')
        stub = git_pb2_grpc.GitStub(channel)

        filename = 'zzz/test/'
        filename +=  file_obj._get_name()
        filedata = file_obj.file.read()

        regex = re.compile(".exe$")
        mo = regex.search(filename)
        filemode = 100644
        if mo != None:
            print(mo.group())
            filemode = 100755

        response = stub.AddOrUpdateFile(git_pb2.Request_File(path="nexivil6/hosuk6/", filedata=filedata, filename=filename, filemode=filemode))
        status = { 'result':response.result}
        return Response(status)


class RepoView(APIView):

    def get(self, request, formant=None):

        channel = grpc.insecure_channel('localhost:50051')
        stub = git_pb2_grpc.GitStub(channel)

        response = stub.GetRepoTree(git_pb2.Request_Path(path="nexivil6/hosuk6"))
        status = {'trees' : response.trees}
        print(type(response.trees[0]))

        trees = response.trees
        print(trees)
        tarr = []
        #serializer = TreeSerializer(response.trees[0])
        #print(serializer.data)
        #json = JSONRenderer().render(serializer.data)
        #tarr.append(json)
        #tarr.append(json)
        serializer = TreeSerializer(trees , many=True)
        json = JSONRenderer().render(serializer.data)
        #print(json)
        # for tree in trees:
        #     serializer = TreeSerializer(tree)
        #     json = JSONRenderer().render(serializer.data)
        #     tarr.append(json)

        #response = JsonResponse(trees,safe=False)

        #dictObj = MessageToDict(trees, preserving_proto_field_name=True)
        #print(dictObj)
        #jsonObj = MessageToJson(dictObj, including_default_value_fields=True)

        #jsonob = json.dumps(trees)

        # for tree in trees:
        #     obj = MessageToJson(tree)
        #     tarr.append(obj)

        #json = JSONRenderer().render(tarr)

        #jsonObj = MessageToJson(trees[1], including_default_value_fields=True)
        
        #tarr.append(jsonObj)
        return Response({'hihi':'wer', 'trees':json})
