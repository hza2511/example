"""
Base serializers.
"""
import sys
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from rest_framework import serializers
from restaurants.models import Domain


class BinaryImageSerializer(serializers.ModelSerializer):
    """
    BinaryImageSerializer validates images and resizes if needed into 640x480.

    Required:
        class Meta:
            model = Model

            fields = ('image', )
    """
    def to_internal_value(self, data):
        # We receive "file" in the request, rename to the "image"
        try:
            data['image'] = data.pop('file')
        except KeyError:
            raise serializers.ValidationError({'file': 'Should not be empty.'})
        return super(BinaryImageSerializer, self).to_internal_value(data)
        
    def validate_image(self, image):
        if isinstance(image, InMemoryUploadedFile) or isinstance(image, TemporaryUploadedFile):
            im = Image.open(image)
            output = BytesIO()

            if image.image.height > 480 or image.image.width > 640:
                im = im.resize((640, 480))
                if im.mode in ("RGBA", "P"):
                    im = im.convert("RGB")
                im.save(output, format='JPEG', quality=100)
                output.seek(0)

                image = InMemoryUploadedFile(output, 'ImageField', "%s.jpeg" % image.name.split('.')[0], 'image/jpeg',
                                             sys.getsizeof(output), None)
            return image


class DomainSerializer(serializers.ModelSerializer):
    """
        Domain Serializer. Read only.
        Returns only domain.
    """
    def to_representation(self, instance):
        return instance.domain

    class Meta:
        model = Domain
        fields = ('domain', )
        read_only_fields = ('domain', )
