from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from core.models import Product, Material
from serilizers import ProductSerializer, ProductMaterialSerializer


class ProductsApiView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.prefetch_related("product_materials__material")
        serializer = self.get_serializer(products, many=True)
        return Response({"result": serializer.data})

    # def post(self, request):
    #     product_name = request.data.get('name')
    #     product = Product.objects.get(name=product_name)
    #
    #     product_material_data = request.data.get('product_materials', [])
    #     for material_data in product_material_data:
    #         material_data['product'] = product.id
    #
    #     serializer = ProductMaterialSerializer(data=product_material_data, many=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     return Response({"success": "New product materials saved"}, status=status.HTTP_201_CREATED)


class ProductsCreateApiView(GenericAPIView):
    serializer_class = ProductMaterialSerializer

    def post(self, request):
        product_name = request.data.get('name')
        product = Product.objects.get(name=product_name)

        product_material_data = request.data.get('product_materials', [])
        for material_data in product_material_data:
            material_name = material_data.pop('material_name', None)
            if material_name:
                material = Material.objects.get_or_create(name=material_name)[0]
                material_data['material'] = material.id
            material_data['product'] = product.id

        serializer = self.get_serializer(data=product_material_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"success": "New product materials saved"}, status=status.HTTP_201_CREATED)
