from rest_framework import serializers
from first_app.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = '__all__'  # mean get all fields
        fields = ['id', 'first_name', 'last_name','email','age','is_active'] # get some fields
        read_only_fields = ['id'] # never change this fields

    def validate_email(self, value):
        """
        custom validation for email field
        """
        # check if we'ar updating an existing instance
        if self.instance:
            # for update: if email is changed, check if it exists for others students
            if self.instance.email !=value:
                if Student.objects.filter(email = value).exists():
                    raise serializers.ValidationError("A student with this email already exists")
        else:
            # for create: check if email exists for any student
            if Student.objects.filter(email = value).exists():  # return True or False
                raise serializers.ValidationError('A student with this email already exists!!!')
        return value
    
    def validate_age(self, value):
        """
        custom validation for age field
        """
        if value < 6 or value > 130:  # value = 18 ==> false | value = 140 ==> true 
            raise serializers.ValidationError('age must be between 6 and 130')
        return value