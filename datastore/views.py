from django.shortcuts import get_object_or_404
from django.db import connection
from psycopg2.extras import DictCursor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timezone

from .serializers import ProductSerializer, StoreSerializer
from .models import Product, Company, Store
from .permissions import OwnerPermissionStore

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def remove_columns(column_names, data):
    return [{x:i[x] for x in i if x in column_names} for i in data]


class StoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        print(data)
        serializer = StoreSerializer(data=data)
        cursor = connection.cursor()

        # Query for inserting title, address, company
        query1 = f"""
                    INSERT INTO 
                        datastore_store (title, address, company_id) 
                    VALUES 
                        ('{data["title"]}', '{data["address"]}', {data["company"]})
                    RETURNING id
        """
        cursor.execute(query1)
        id_of_new_row = [cursor.fetchone()[0]] * len(data['products'])

        query2 = f"""
            INSERT INTO 
                datastore_store_products (store_id, product_id) 
            VALUES {','.join(str(x) for x in zip(id_of_new_row, data['products']))}
        """
        cursor.execute(query2)
        cursor.close()
        return Response({
                "status": "success",
                "data": data
            },
            status=status.HTTP_200_OK)

    
    def get(self, request, id=None):
        if id:
            query = f""" SELECT 
                            datastore_store.id, datastore_store.title, datastore_store.address, 
                            datastore_store.company_id, datastore_company.id,datastore_company.title, 
                            datastore_company.manager_id, datastore_manager.id, datastore_manager.user_id, 
                            auth_user.id, auth_user.username,                            
                            ARRAY (SELECT 
                                    datastore_product.title
                                FROM 
                                    datastore_product 
                                INNER JOIN 
                                    datastore_store_products 
                                ON 
                                    (datastore_product.id = datastore_store_products.product_id) 
                                WHERE datastore_store_products.store_id = datastore_store.id)
                            AS products                            
                            FROM datastore_store 
                            INNER JOIN datastore_company 
                                ON datastore_store.company_id = datastore_company.id 
                            INNER JOIN datastore_manager 
                                ON datastore_company.manager_id = datastore_manager.id 
                            INNER JOIN auth_user 
                                ON datastore_manager.user_id = auth_user.id
                            WHERE auth_user.id = {request.user.id}
                            AND datastore_store,id = {id}; 
                    """    
        else:
            query = f""" SELECT 
                            datastore_store.id, datastore_store.title, datastore_store.address, 
                            datastore_store.company_id, datastore_company.id,datastore_company.title, 
                            datastore_company.manager_id, datastore_manager.id, datastore_manager.user_id, 
                            auth_user.id, auth_user.username,                            
                            ARRAY (SELECT 
                                    datastore_product.title
                                FROM 
                                    datastore_product 
                                INNER JOIN 
                                    datastore_store_products 
                                ON 
                                    (datastore_product.id = datastore_store_products.product_id) 
                                WHERE datastore_store_products.store_id = datastore_store.id)
                            AS products
                            FROM datastore_store 
                            INNER JOIN datastore_company 
                                ON datastore_store.company_id = datastore_company.id 
                            INNER JOIN datastore_manager 
                                ON datastore_company.manager_id = datastore_manager.id 
                            INNER JOIN auth_user 
                                ON datastore_manager.user_id = auth_user.id
                            WHERE auth_user.id = {request.user.id}; 
                    """
        columns = ["id", "title", "address", "products"]
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = dictfetchall(cursor)
            row = remove_columns(columns, row)
            return Response({
                    "status": "success",
                    "data": row,
                },
                status=status.HTTP_200_OK
            )

        # item = Store.objects.select_related()
        # serializer = StoreSerializer(item, many=True)

        # return Response({
        #         "status": "success",
        #         "data": serializer.data,
        #     },
        #     status=status.HTTP_200_OK
        # )

class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data
        # serializer = ProductSerializer(data=data)
        print(request.data)
        query = f"""
                    INSERT INTO datastore_product
                        (barcode, title, description, price, 
                        quantity, date_added, last_updated, 
                        company_id) 
                    VALUES
                        ('{data["barcode"]}', '{data["title"]}', '{data["description"]}', 
                        {data["price"]}, {data["quantity"]}, 
                        '{datetime.now(timezone.utc)}'::timestamptz, '{datetime.now(timezone.utc)}'::timestamptz,
                        {data["company"]})
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            return Response({
                    "status": "success",
                    "data": data,
                },
                status=status.HTTP_200_OK
            )

    def get(self, request, id=None):
        if id:
            query = f'''SELECT 
                            datastore_product.id, datastore_product.barcode, 
                            datastore_product.title, datastore_product.description, 
                            datastore_product.price, datastore_product.quantity, 
                            datastore_product.date_added, datastore_product.last_updated, 
                            datastore_product.company_id, datastore_company.id,
                            datastore_company.title as company_name, datastore_company.manager_id, 
                            datastore_manager.id, datastore_manager.user_id, auth_user.id 
                        FROM datastore_product 
                        INNER JOIN datastore_company 
                            ON (datastore_product.company_id = datastore_company.id) 
                        INNER JOIN datastore_manager 
                            ON (datastore_company.manager_id = datastore_manager.id) 
                        INNER JOIN auth_user 
                            ON (datastore_manager.user_id = auth_user.id)
                        WHERE auth_user.id = {request.user.id}
                        AND datastore_product.id = {id};    
                '''    
        else:
            query = f'''SELECT 
                            datastore_product.id, datastore_product.barcode, 
                            datastore_product.title, datastore_product.description, 
                            datastore_product.price, datastore_product.quantity, 
                            datastore_product.date_added, datastore_product.last_updated, 
                            datastore_product.company_id, datastore_company.id,
                            datastore_company.title as company_name, datastore_company.manager_id, 
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
        columns = ["id", "barcode", "title", "description", "price", "quantity", "date_added", "last_updated", "company_name"]
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = dictfetchall(cursor)
            row = remove_columns(columns, row)
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
                        auth_user.id, auth_user.username
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