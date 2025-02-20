from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .models import Movie
from .permissions import IsOwnerOrReadOnly
from .serializers import MovieSerializer
from .pagination import CustomPagination
from .filters import MovieFilter


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class TheatreView(APIView):
    def get(self, request):
        theatres = Theatre.objects.all()
        data = [{"name": theatre.name, "location": theatre.location} for theatre in theatres]
        return JsonResponse(data, safe=False)

    def post(self, request):
        theatre = Theatre.objects.create(
            name=request.data.get('name'),
            location=request.data.get('location'),
            capacity=request.data.get('capacity', -1),
            opening_date=request.data.get('opening_date')
        )
        return JsonResponse({"message": "Theatre created", "id": theatre.id})

    def delete(self, request):
        theatre_id = request.GET.get('id')
        Theatre.objects.filter(id=theatre_id).delete()
        return JsonResponse({"message": "Theatre deleted"})
