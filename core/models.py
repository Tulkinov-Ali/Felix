from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, related_name='product_materials', on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.product.name


@receiver(post_save, sender=ProductMaterial)
def update_material_quantity(sender, instance, **kwargs):
    if instance.pk is None:
        material = instance.material
        quantity_needed = instance.quantity
        used_materials = []
        warehouses = Warehouse.objects.all().order_by('id')
        for warehouse in warehouses:
            available_quantity = \
                warehouse.materials.filter(name=material.name).aggregate(total_quantity=models.Sum('quantity'))[
                    'total_quantity']
            if available_quantity is not None and available_quantity >= quantity_needed:
                warehouse_materials = warehouse.materials.filter(name=material.name)
                for wm in warehouse_materials:
                    if quantity_needed > 0:
                        if wm.quantity >= quantity_needed:
                            wm.quantity -= quantity_needed
                            wm.save()
                            used_materials.append((warehouse.id, wm.quantity))
                            quantity_needed = 0
                        else:
                            quantity_needed -= wm.quantity
                            wm.quantity = 0
                            wm.save()
                            used_materials.append((warehouse.id, wm.quantity))
            if quantity_needed == 0:
                break

        if quantity_needed > 0:
            used_materials.append((None, quantity_needed))
            ProductMaterial.objects.create(
                product=instance.product,
                warehouse_id=None,
                material=instance.material,
                quantity=quantity_needed,
                price=None
            )
