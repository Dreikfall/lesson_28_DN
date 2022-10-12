import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from users.models import User, Location


class UserListView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('username')

        users = []
        for user in self.object_list:
            users.append(
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "password": user.password,
                    "role": user.role,
                    "age": user.age,
                    "total_ads": user.ad_set.count()
                })
        return JsonResponse(users, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "password": user.password,
                    "role": user.role,
                    "age": user.age,
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'first_name', 'last_name',
              'password', 'role', 'locations', 'age']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        user = User.objects.create(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role'],
            password=data['password'],
            age=data['age']
        )
        for loc in data['locations']:
            location, _ = Location.objects.get_or_create(name=loc)
            user.location.add(location)

        return JsonResponse({'id': user.id,
                             'username': user.username,
                             'first_name': user.first_name,
                             "last_name": user.last_name,
                             'role': user.role,
                             'password': user.password,
                             'age': user.age,
                             'locations': [str(u) for u in user.location.all()]
                             })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name',
              'password', 'role', 'locations', 'age']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)


        locations = get_object_or_404(Location, id=data['locations'])

        self.object.username = data['username']
        self.object.first_name = data['first_name']
        self.object.last_name = data['last_name']
        self.object.role = data['role']
        self.object.password = data['password']
        self.object.age = data['age']
        self.object.locations = locations
        self.object.save()
        return JsonResponse(
            {
                "id": self.object.id,
                "username": self.object.username,
                "first_name": self.object.first_name,
                "last_name": self.object.last_name,
                "role": self.object.role,
                "password": self.object.password,
                "age": self.object.age,
                "locations": # вот здесь я встрял
            }
         )


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)
