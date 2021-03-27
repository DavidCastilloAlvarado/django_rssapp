from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import Add_feed_user, Id_feed_serializer, log_serializer
from rest_framework import status
from django.contrib.auth.models import User
from .models import User_feed
from .utiles import get_items_from_feed


@login_required()
def rss_view(request):
    query_feeds = User_feed.objects.filter(author=request.user.username)
    context = {
        "username": request.user.username,
        "feeds": query_feeds
    }
    return render(request, 'rssapp/home.html', context)


@login_required()
def rss_add(request):
    query_feeds = User_feed.objects.filter(author=request.user.username)
    #query_feeds = getfeeds_serializer(query_feeds, many=True)
    return render(request, 'rssapp/add_feed.html', {"feeds": query_feeds, })


class API_rss(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_income = Add_feed_user
    serializer_income_delete = Id_feed_serializer
    Get_items_from_feed = get_items_from_feed
    Log_serializer = log_serializer
    user = User

    def get(self, request, form=None):
        """
        Deliver the entire feeds and entries owned by the client.
        """
        query_feeds = User_feed.objects.filter(author=request.user.username
                                               ).values_list("id", "url")
        data = list(query_feeds)
        if len(data) > 0:
            retrieve = []
            for feed in data:
                feed_ = dict()
                feed_["id"] = feed[0]
                feed_["items"] = self.Get_items_from_feed(url=feed[1],
                                                          id=feed[0],
                                                          serializer=self.Log_serializer)
                retrieve.append(feed_)
            return Response(retrieve, status=status.HTTP_200_OK)
        else:
            return Response(
                "No feeds found",
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, format=None):
        """
        Delete a feed by the client. Only his personal feeds
        """
        serializer = self.serializer_income_delete(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            id = serializer.validated_data.get("id")
            # print(id)
            try:
                User_feed.objects.filter(id=id,
                                         author=request.user.username).delete()
                return Response(request.data,
                                status=status.HTTP_200_OK)
            except:
                return Response(
                    "Error query",
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

    def post(self, request, format=None):
        """save the feed of the client"""
        serializer = self.serializer_income(data=request.data,
                                            author=request.user.username)
        # print(serializer)
        if serializer.is_valid():
            #title = serializer.validated_data.get("title")
            # print(title)
            try:
                serializer.save()
                return Response(request.data,
                                status=status.HTTP_200_OK)
            except:
                return Response(
                    "Error query",
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
