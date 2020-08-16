from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from django.conf import settings
from django.contrib.auth import login
from rest_pyotp.views import PyotpViewset
from rest_pyotp import  models
from users.models import User
from users.messages import otp_generate_message
from users.utils import send_txt





class UserLoginGenerateOTP(PyotpViewset):

    # verify if user exists and obtain user object
    def get_user(self,mobile):
        try:
            user = User.objects.get(mobile=mobile)
            return user
        except User.DoesNotExist:
            raise Http404


    def generate_totp(self, request):
        """
        """
        try:
            user = self.get_user(request.data['mobile'])
            serializer = self.get_serializer_class()
            serializer = self._validate(serializer, {'time':settings.OTP_TIME_EXP})

            # save uuid generated from rest_pyotp on serializer and save on user 
            # object(update user record with uuid) and send otp via sms

            User.objects.filter(id=user.id).update(otp_token_uuid=serializer['otp_uuid'])

            message = otp_generate_message(serializer['otp'])
            print('message: ',message)
            send_txt(request.data['mobile'],message)

            return Response({'success':"otp dilivered successfully"},status=status.HTTP_201_CREATED)
        except KeyError as err:
            return Response({'error': str(err) + ' is a required field'},status=status.HTTP_400_BAD_REQUEST)



    

    def verify_otp(self, request):
        

        
        try:
            self.user = self.get_user(request.data['mobile'])
            uuid = self.user.otp_token_uuid

            # obj = self.get_object()
            uuid = models.PyOTP.objects.get(uuid=uuid)
            serializer = self.get_serializer_class()

            serializer = serializer(data={'otp':request.data['otp']})
            serializer.is_valid(raise_exception=True)

            valid_otp = serializer.verify_otp(serializer.data.get('otp'), uuid, settings.OTP_TYPE)
            if not valid_otp:
                return Response({'error':'invalid otp code'},status=status.HTTP_400_BAD_REQUEST)
            # log user in on verification success
            login(request, self.user,backend='django.contrib.auth.backends.ModelBackend')


            return Response({'success':"user successfully logged in"})

        except KeyError as err:
            return Response({'error': str(err) + ' is a required field'},status=status.HTTP_400_BAD_REQUEST)


