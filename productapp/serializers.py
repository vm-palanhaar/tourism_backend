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
    cat = serializers.CharField()
    images = serializers.SerializerMethodField()
    class Meta:
        model = models.Prod
        fields = ('id','brand','name','image','images','desc','price','cat','weight')

    def get_images(self, instance):
        images = ProductImageSerializer(models.ProdImg.objects.filter(prod=instance), many=True).data
        return images

class AddOrgSerializer_iDukaan(serializers.ModelSerializer):
    class Meta:
        model = models.Org
        fields = ('name','address')

    def create(self, validated_data):
        return super().create(validated_data)


class OrgListSerializer_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.Org
        fields = ('id','name')

class AddBrandSerializer_iDukaan(serializers.ModelSerializer):
    confirm = serializers.BooleanField(required=True)
    org_id = serializers.CharField(required=True,  allow_null=True)
    class Meta:
        model = models.Brand
        fields = ('name','image','confirm','org_id')

    def create(self, validated_data):
        brand = models.Brand.objects.create(
            name = validated_data['name'],
            image = validated_data['image'],
            is_active = False,
            is_show = False,
        )
        brand.save()
        orgs_id = self.context.get('orgs_id')
        orgs_id = orgs_id.replace("[","").replace("]","").replace("\"","").replace("\'","").split(",")
        for org_id in orgs_id:
            org = models.Org.objects.get(id = org_id)
            org_brand = models.OrgBrand.objects.create(
                org = org,
                brand = brand
            )
            org_brand.save()
        return brand


class BrandListSerializer_iDukaan(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.Brand
        exclude = ['created_at','updated_at','is_show',]

class ProductSubCatListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.ProdSubCat
        exclude = ['cat','desc']

class ProductMacroCatListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    class Meta:
        model = models.ProdMacroCat
        exclude = ['cat','sub_cat','desc']

class ProductCatListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    sub_cat = serializers.SerializerMethodField()
    class Meta:
        model = models.ProdCat
        fields = ['id','name','sub_cat']

    def get_sub_cat(self, obj):
        response_data = []
        sub_cats = models.ProdSubCat.objects.filter(cat = obj)
        for sub_cat in sub_cats:
            macro_cats = models.ProdMacroCat.objects.filter(sub_cat = sub_cat, cat = obj)
            serializer_macro_cats = ProductMacroCatListSerializer(macro_cats, many = True)
            serializer_sub_cat = ProductSubCatListSerializer(sub_cat)
            response_map = serializer_sub_cat.data
            if serializer_macro_cats.data != None:
                response_map['macro_cat'] = serializer_macro_cats.data
            response_data.append(response_map)
        return response_data
    


class ProductImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = models.ProdImg
        fields = ('id','image',)


class AddProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False, read_only=True)
    confirm = serializers.BooleanField(required=False, read_only=True)
    images = ProductImageSerializer(required=False, allow_null=True, many=True)
    class Meta:
        model = models.Prod
        fields = ('id','brand','name','image','desc','price','cat','sub_cat','macro_cat','images','confirm','net_weight')

    def create(self, validated_data):
        try:
            images = self.context.get('images')
        except KeyError:
            return super().create(validated_data)

        product = models.Prod.objects.create(**validated_data)
        for image in images:
            models.ProdImg.objects.create(product=product,image=image)
        return product
    

class ProductListSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    cat = serializers.CharField()
    brand = serializers.SerializerMethodField()
    class Meta:
        model = models.Prod
        fields = ('id','brand','name','image','price','cat','is_active','net_weight')

    def get_brand(self, instance):
        if instance.brand.is_show == False:
            return None
        return f'{instance.brand.name}'
    

class PatchProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    price = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    class Meta:
        model = models.Prod
        fields = ('id','image','price','description','weight')


# class ProductSubGroupListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.ProductSubGroup
#         fields = ['name','id']


# class ProductGroupListSerializer(serializers.ModelSerializer):
#     subgroups = serializers.SerializerMethodField()
#     class Meta:
#         model = models.ProductGroup
#         fields = ['name','subgroups']

#     def get_subgroups(self, instance):
#         subgroups = models.ProductSubGroup.objects.filter(group=instance)
#         return ProductSubGroupListSerializer(subgroups, many=True).data
