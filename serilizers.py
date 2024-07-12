from rest_framework import serializers
from core.models import Product, ProductMaterial


class ProductMaterialSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.name', read_only=True)

    class Meta:
        model = ProductMaterial
        fields = ('warehouse_id', 'material_name', 'quantity', 'price')


class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'quantity', 'product_materials')
