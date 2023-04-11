from rest_framework import serializers

from productapp import models


'''
Common APIs Serializer
1. ProductSerializer [ProductImageSerializer]

iDukaan APIs Serializer
1. AddBrandSerializer
2. BrandListSerializer
3. ProductCatergoryListSerializer
4. AddProductSerializer [ProductImageSerializer]
5. ProductListSerializer
'''


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    brand = serializers.CharField()
    category = serializers.CharField()
    images = serializers.SerializerMethodField()
    class Meta:
        model = models.Product
        fields = ('id','brand','name','image','images','description','price','category')

    def get_images(self, instance):
        images = ProductImageSerializer(models.ProductImage.objects.filter(product=instance), many=True).data
        return images


class AddBrandSerializer(serializers.ModelSerializer):
    confirm = serializers.BooleanField(required=False, read_only=True)
    class Meta:
        model = models.Brand
        fields = ('name','image','confirm')


class BrandListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.Brand
        exclude = ['created_at','updated_at','is_show',]


class ProductCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = models.ProductImage
        fields = ('id','image',)


class AddProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False, read_only=True)
    confirm = serializers.BooleanField(required=False, read_only=True)
    images = ProductImageSerializer(required=False, allow_null=True, many=True)
    class Meta:
        model = models.Product
        fields = ('id','brand','name','image','description','price','category','images','confirm')

    def create(self, validated_data):
        try:
            images = self.context.get('view').request.FILES.getlist('images')
        except KeyError:
            return super().create(validated_data)

        product = models.Product.objects.create(**validated_data)
        for image in images:
            models.ProductImage.objects.create(product=product,image=image)
        return product
    

class ProductListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    category = serializers.CharField()
    brand = serializers.SerializerMethodField()
    class Meta:
        model = models.Product
        fields = ('id','brand','name','image','price','category','is_active')

    def get_brand(self, instance):
        if instance.brand.is_show == False:
            return None
        return f'{instance.brand.name}'
    

class PatchProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    price = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    class Meta:
        model = models.Product
        fields = ('id','image','price','description')
