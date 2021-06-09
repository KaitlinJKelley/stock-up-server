import json
from stockupapi.models.employee import Employee
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from stockupapi.models import Company
from rest_framework import status


@csrf_exempt
def login_user(request):

    req_body = json.loads(request.body.decode())

    if request.method == 'POST':

        username = req_body['username']
        password = req_body['password']
        # Verifies the user exists with the username/password combo
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            # Returns token to client
            return HttpResponse(data, content_type='application/json')

        else:
            # Login combo didn't match any user
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')

@csrf_exempt
def register_user(request):

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    company = Company.objects.create(
        company_name = req_body["companyName"],
        ein = req_body["ein"],
        report_view = req_body["reportView"],
        order_schedule = req_body["orderSchedule"],
        cat_pref = req_body["catPref"],
        logo = None
    )

    company.save()

    employee = Employee.objects.create(
        employee_id=req_body['employeeId'],
        company = company,
        user=new_user
    )

    employee.save()

    token = Token.objects.create(user=new_user)

    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json', status=status.HTTP_201_CREATED)
    