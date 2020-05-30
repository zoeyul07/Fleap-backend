import re
import jwt
import bcrypt
import json
import requests
import datetime

from django.views       import View
from django.http        import HttpResponse, JsonResponse
from django.db          import IntegrityError
from django.db.models   import Avg
from django.utils       import timezone

from .models            import User, UserFrip, Interest, InterestDetail, Review, Purchase
from frip.models        import Frip, SubRegion, Image
from .utils             import login_check

from fleap.settings import SECRET_KEY, ALGORITHM


EMAIL_REGEX = r"^[a-zA-Z0-9!#$%^&*\-_=+{}]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$"
PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@.#^* ?+=_~])[A-Za-z\d!@.#^* ?+=_~]{8,}$"

class SignUpView(View):
    VALIDATION_RULES = {
        'email': lambda email: False if not re.match(EMAIL_REGEX, email) else True,
        'password': lambda password: False if not re.match(PASSWORD_REGEX, password) else True
    }

    def post(self, request):
        try:
            data = json.loads(request.body)
            if len(data.keys()) != 2:
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
                    token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
                    return JsonResponse({"token": token}, status=200)
                return HttpResponse(status=401)
            return HttpResponse(status=401)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

class KakaoView(View):
    def post(self, request):
        token = request.headers['Authorization']

        if not token:
            return JsonResponse({'message':'TOKEN_REQUIRED'}, status=400)

        user_request = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization':f'Bearer {token}'})
        user_information = user_request.json()['properties']
        kakao_id = user_request.json()['id']
        nickname = user_information.get('nickname', None)

        if User.objects.filter(kakao_id=kakao_id).exists():
            user = User.objects.get(kakao_id=kakao_id)
            access_token= jwt.encode({'id':user.id}, SECRET_KEY, ALGORITHM)
            
            return JsonResponse({'access_token':access_token.decode('utf-8'), 'nickname':user.kakao_name}, status=200)

        else:
            user = User.objects.create(
                kakao_id = kakao_id,
                kakao_name = nickname
            )

            access_token = jwt.encode({'id':user.id}, SECRET_KEY, ALGORITHM)

            return JsonResponse({'access_token':access_token.decode('utf-8'),'nickname':nickname}, status=200)

class LikeView(View):
    @login_check
    def post(self,request):
        try:
            data = json.loads(request.body)
            like=int(data['like'])
            user_id  = request.user.id
            frip_id  = data['frip_id']

            if UserFrip.objects.filter(user_id=user_id, frip_id=frip_id).exists():
                UserFrip.objects.filter(
                    user_id  = request.user.id,
                    frip_id  = data['frip_id']
                ).delete()
            elif  UserFrip.objects.filter(user_id=user_id, frip_id=frip_id).exists():
                UserFrip.objects.create(
                    user_id  = request.user.id,
                    frip_id = data['frip_id'])
            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"},status=401)

class InterestCategoryView(View):
    def get(self,request):
        interests=Interest.objects.all()
        interest_list=[
            {"id":interest.id,
             "name":interest.name,
             "data":[{"id":detail.id,
                      "name":detail.name}for detail in InterestDetail.objects.filter(interest_id=interest)]}for interest in interests]

        return JsonResponse({"data":interest_list},status=200)