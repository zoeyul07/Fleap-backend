import re
import jwt
import bcrypt
import json

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError

from .models import User
from fleap.settings import SECRET_KEY


class SignUpView(View):
    VALIDATION_RULES = {
        'email': lambda email: False if not re.match(r"^[a-zA-Z0-9!#$%^&*\-_=+{}]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$", email) else True,
        'password': lambda password: False if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@.#^* ?+=_~])[A-Za-z\d!@.#^* ?+=_~]{8,}$", password) else True
    }

    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "ALREADY_EXISTS"}, status=400)

            if len(data.keys()) < 2:
                return HttpResponse(status=400)
            for value in data.values():
                if value in "":
                    return HttpResponse(status=400)

            for field, validator in self.VALIDATION_RULES.items():
                if not validator(data[field]):
                    return HttpResponse(status=400)

            User.objects.create(
                email=data['email'],
                password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            )
            return HttpResponse(status=200)

        except IntegrityError:
            return JsonResponse({"message": "DUPLICATED_KEYS"}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'email': user.email}, SECRET_KEY, algorithm='HS256').decode('utf-8')
                    return JsonResponse({"token": token}, status=200)
                return HttpResponse(status=401)
            return HttpResponse(status=401)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)
