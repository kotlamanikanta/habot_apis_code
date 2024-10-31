# serializers.py
import re
from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        error_messages={
            'blank': 'name should not be empty.',
        }
    )
    class Meta:
        model = Employee
        fields = '__all__'  # Or specify specific fields as a list

    def validate_email(self, value):
        """Check that the email is unique and valid."""
        # Regular expression for validating an Email
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        print(self.initial_data,"jflkfkfg")
        # Check if the email matches the regex
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format.")
        
        # Check for uniqueness
        if Employee.objects.filter(email=value).exists() and self.initial_data["email"] !=value:
            raise serializers.ValidationError("This email is already in use.")
        
        return value

    def validate_name(self, value):
        """Check that the name is not empty."""
        if not value or value.strip() == "":
            raise serializers.ValidationError("name should not be empty.")
        
        return value
