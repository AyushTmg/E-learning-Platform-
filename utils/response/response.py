from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST


# ! For Custom Response 
class  CustomResponse:

    @staticmethod
    def success(data="",message="Successful",status=HTTP_200_OK) -> Response:
        """
        This custom method is used to return successful
        response 
        """
        return Response({
                "data":data,
                "success":True,
                "message":message
            },
            status=status
        )
    

    @staticmethod
    def error(data="",message="Error",status=HTTP_400_BAD_REQUEST) -> Response:
        """
        This custom method is used to return error
        response 
        """
        return Response({
            "data":data,
            "success":False,
            "message":message
        },
        status=status
    )