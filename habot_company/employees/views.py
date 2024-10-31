from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Employee
from .serializers import EmployeeSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employee_operations(request, id=None):
    if request.method == 'GET':
        if id:
            try:
                employee = Employee.objects.get(id=id)
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data)
            except Employee.DoesNotExist:
                return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        # Filtering based on department and role (optional)
        department = request.query_params.get('department')
        role = request.query_params.get('role')
        employees = Employee.objects.all()
        if department:
            employees = employees.filter(department__iexact=department)
        if role:
            employees = employees.filter(role__iexact=role)

        # Paginate the queryset
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Override per-page limit
        paginated_employees = paginator.paginate_queryset(employees, request)

        # Serialize the paginated data
        serializer = EmployeeSerializer(paginated_employees, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {'message': 'Employee details create successfully', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(instance=employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Employee details Update successfully','data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            employee = Employee.objects.get(id=id)
            employee.delete()
            return Response({'message': 'Employee deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)