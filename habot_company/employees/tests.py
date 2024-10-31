from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeTests(APITestCase):
    def setUp(self):
        # Set up user and authentication
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)

        # Create initial test employees
        self.employee1 = Employee.objects.create(name="Alice", email="alice@example.com", department="IT", role="Developer")
        self.employee2 = Employee.objects.create(name="Bob", email="bob@example.com", department="HR", role="Manager")
        
        # URLs for testing
        self.list_create_url = reverse('employees:employee_operations')  # For GET all and POST
        self.detail_url = lambda id: reverse('employees:employee_detail', args=[id])  # For GET, PUT, DELETE by ID

    def test_list_employees(self):
        response = self.client.get(self.list_create_url)
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_filter_employees_by_department(self):
        response = self.client.get(self.list_create_url, {'department': 'IT'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(emp['department'] == 'IT' for emp in response.data['results']))

    def test_get_employee_detail(self):
        response = self.client.get(self.detail_url(self.employee1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.employee1.name)

    def test_get_employee_not_found(self):
        response = self.client.get(self.detail_url(999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_employee(self):
        data = {
            "name": "Charlie",
            "email": "charlie@example.com",
            "department": "Finance",
            "role": "Analyst"
        }
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], data['name'])

    def test_create_employee_with_existing_email(self):
        data = {
            "name": "Duplicate Email",
            "email": "alice@example.com",  # Already exists
            "department": "IT",
            "role": "Developer"
        }
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_update_employee(self):
        data = {
            "name": "Alice Updated",
            "email": "alice@example.com",
            "department": "IT",
            "role": "LeadDeveloper"
        }
        response = self.client.put(self.detail_url(self.employee1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee1.refresh_from_db()
        self.assertEqual(self.employee1.name, data['name'])

    def test_update_employee_not_found(self):
        data = {"name": "Non-existent", "email": "nonexistent@example.com"}
        response = self.client.put(self.detail_url(999), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_employee(self):
        response = self.client.delete(self.detail_url(self.employee1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(id=self.employee1.id).exists())

    def test_delete_employee_not_found(self):
        response = self.client.delete(self.detail_url(999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
