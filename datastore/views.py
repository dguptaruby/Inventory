from django.shortcuts import get_object_or_404
from django.db import connection
from psycopg2.extras import DictCursor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerializer, StoreSerializer
from .models import Product, Company, Store
from .permissions import OwnerPermissionStore

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class StoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            },
            status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "data": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id=None):
        query = f""" SELECT 
                        datastore_store.id, datastore_store.title, datastore_store.address, 
                        datastore_store.company_id, datastore_company.id,datastore_company.title, 
                        datastore_company.manager_id, datastore_manager.id, datastore_manager.user_id, 
                        auth_user.id, auth_user.username,
                        (SELECT title as products FROM datastore_product WHERE datastore_product.company_id = datastore_company.id)
                    FROM datastore_store 
                    INNER JOIN datastore_company ON datastore_store.company_id = datastore_company.id 
                    INNER JOIN datastore_manager ON datastore_company.manager_id = datastore_manager.id 
                    INNER JOIN auth_user ON datastore_manager.user_id = auth_user.id
                    WHERE auth_user.id = {request.user.id}; 
                """

        with connection.cursor() as cursor:
            cursor.execute(query)
            row = dictfetchall(cursor)
            return Response({
                    "status": "success",
                    "data": row,
                },
                status=status.HTTP_200_OK
            )

class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            },
            status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "data": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id=None):
        query = f'''SELECT 
                        datastore_product.id, datastore_product.barcode, 
                        datastore_product.title, datastore_product.description, 
                        datastore_product.price, datastore_product.quantity, 
                        datastore_product.date_added, datastore_product.last_updated, 
                        datastore_product.company_id, datastore_company.id,
                        datastore_company.title as comapny_name, datastore_company.manager_id, 
                        datastore_manager.id, datastore_manager.user_id, auth_user.id 
                    FROM datastore_product 
                    INNER JOIN datastore_company 
                    ON (datastore_product.company_id = datastore_company.id) 
                    INNER JOIN datastore_manager 
                    ON (datastore_company.manager_id = datastore_manager.id) 
                    INNER JOIN auth_user 
                    ON (datastore_manager.user_id = auth_user.id)
                    WHERE auth_user.id = {request.user.id};
        '''
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = dictfetchall(cursor)

            return Response({
                    "status": "success",
                    "data": row,
                },
                status=status.HTTP_200_OK
            )

class ProductAnalytics(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = f'''SELECT 
                        datastore_product.id, datastore_product.barcode, 
                        datastore_product.title, datastore_product.description, 
                        datastore_product.price, datastore_product.quantity, 
                        datastore_product.date_added, datastore_product.last_updated, 
                        datastore_product.company_id, datastore_company.id,
                        datastore_company.title as comapny_name, datastore_company.manager_id, 
                        datastore_manager.id, datastore_manager.user_id, auth_user.id 
                    FROM datastore_product 
                    INNER JOIN datastore_company 
                    ON (datastore_product.company_id = datastore_company.id) 
                    INNER JOIN datastore_manager 
                    ON (datastore_company.manager_id = datastore_manager.id) 
                    INNER JOIN auth_user 
                    ON (datastore_manager.user_id = auth_user.id)
                    WHERE auth_user.id = {request.user.id};
        '''
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = dictfetchall(cursor)

            return Response({
                    "status": "success",
                    "data": row,
                },
                status=status.HTTP_200_OK
            )

class StoreAnalytics(APIView):

    def get(self, request):
        query = f""" SELECT 
                        datastore_store.id, datastore_store.title, datastore_store.address, 
                        datastore_store.company_id, datastore_company.id,datastore_company.title, 
                        datastore_company.manager_id, datastore_manager.id, datastore_manager.user_id, 
                        auth_user.id, auth_user.username,
                        (SELECT title as products FROM datastore_product WHERE datastore_product.company_id = datastore_company.id)
                    FROM datastore_store 
                    INNER JOIN datastore_company ON datastore_store.company_id = datastore_company.id 
                    INNER JOIN datastore_manager ON datastore_company.manager_id = datastore_manager.id 
                    INNER JOIN auth_user ON datastore_manager.user_id = auth_user.id
                    WHERE auth_user.id = {request.user.id}; 
                """

        with connection.cursor() as cursor:
            cursor.execute(query)
            row = dictfetchall(cursor)
            return Response({
                    "status": "success",
                    "data": row,
                },
                status=status.HTTP_200_OK
            )