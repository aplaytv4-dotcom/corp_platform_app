from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsAdmin
from common.selectors import app_info


class HealthcheckView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response(app_info())
