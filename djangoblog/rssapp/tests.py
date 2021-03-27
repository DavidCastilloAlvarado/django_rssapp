from django.test import TestCase
from .utiles import get_rss_link, get_items_from_feed
from .serializer import Add_feed_user, Id_feed_serializer, log_serializer
from accounts.serializers import User_Serializers
from rest_framework.test import APITestCase
from .models import User_feed, log_errors
from django.contrib.auth.models import User
from rest_framework import status
import time
# I select New york times because have more that 60 items
# web page to contain a rss into his source code
URL_TO_DETECT_RSS_VAL = "https://www.nytimes.com/"
# Rss validated, it works
RSS_VAL = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"


class MultiTestFeedsCases(TestCase):
    def setUp(self):
        self.data = dict(
            title="This is a test feed",
            body="this is the body o description",
            url=RSS_VAL,
        )
        self.data_2 = self.data.copy()
        self.data_2["url"] = URL_TO_DETECT_RSS_VAL

        self.userdata = {'username': 'dave5',
                         'first_name': 'david',
                         'last_name': 'castillo',
                         'email': 'dcastilloa@uni.pe',
                         'password_1': 'TnLM17gr9nFNQnl',
                         'password_2': 'TnLM17gr9nFNQnl', }
        self.bad_userdata = self.userdata.copy()
        self.bad_userdata['password_2'] = 'TnLM17gr9nFN'

    def create_user(self, mode='good'):
        if mode == 'good':
            request = self.client.post('/accounts/signup/', self.userdata)
        elif mode == 'fail':
            request = self.client.post('/accounts/signup/', self.bad_userdata)
        return request

    def login_user(self):
        response = self.client.post('/accounts/login/',
                                    {'username': self.userdata['username'],
                                     'password': self.userdata['password_2'], })
        return response

    def user_signup_login(self):
        response = self.create_user()
        response = self.login_user()
        return response

    def test_get_rss_link(self,):
        rss, state = get_rss_link(URL_TO_DETECT_RSS_VAL)
        self.assertEqual(rss, RSS_VAL)
        self.assertTrue(state)

    def test_get_items_from_feed(self,):
        """
        Test the function which get the items or entries from the feeds,
        the function take the url (rss) from de database and then request
        the data to the source, parse xml and transform the first 8 entries into json format
        """
        class OBJ:
            get_items_from_feed = get_items_from_feed
        obj = OBJ()
        result = obj.get_items_from_feed(url=RSS_VAL,
                                         id=999,
                                         first=1,
                                         serializer=log_serializer)
        self.assertEqual(len(result), 5)

    def test_get_items_from_feed_more_update(self,):
        """
        Test the function which get the items or entries from the feeds,
        the function take the url (rss) from de database and then request
        the data to the source, parse xml and transform the first 8 entries into json format
        """
        class OBJ:
            get_items_from_feed = get_items_from_feed
        obj = OBJ()
        result = obj.get_items_from_feed(url=RSS_VAL,
                                         id=999,
                                         first=0,
                                         serializer=log_serializer)
        self.assertEqual(len(result), 7)

    def test_get_items_from_feed_raising_error_then_save_log(self,):
        """
        Test how the register log error works, when a error occurs,
        requested the rss source the error is register into the table 
        log_errors, saving the id of the feed and the url
        """
        class OBJ:
            get_items_from_feed = get_items_from_feed
        obj = OBJ()
        result = obj.get_items_from_feed(url=RSS_VAL[:-3],
                                         id=999,
                                         first=1,
                                         serializer=log_serializer)
        self.assertEqual(len(result), 0)
        self.assertTrue(log_errors.objects.filter(id_feed=999).exists())

    def test_user_feed_model_serializer(self,):
        """
        Testing the serializer used to create a record in the feed table,
        then continue with saving the data serialized into the model.
        User_feed. Finaly ask to the model if the record exist.
        """
        author = "david"
        data = dict(
            title="This is a test feed",
            body="this is the body o description",
            url=RSS_VAL,
        )
        serializer = Add_feed_user(data=data, author=author)
        if serializer.is_valid():
            serializer.save()
        self.assertTrue(User_feed.objects.filter(url=data["url"],
                                                 author=author).exists())

    def test_adding_feed_rss_exposed(self):
        """
        Test the Api for add new user's feed, end to end, using a url which is
        already a rss source link.
        - post request to the API
        - serializer validation
        - status_code validations 200
        - ask to the database if the record exist
        """
        response = self.user_signup_login()
        response = self.client.post('/rss/api/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User_feed.objects.filter(url=self.data["url"],
                                                 author=self.userdata['username']).exists())

    def test_adding_feed_rss_to_search(self):
        """
        Test the Api for add new user's feed, end to end, using a url which 
        is not a source of rss, bur we can autodetect its rss_url
        - post request to the API
        - serializer validation
        - status_code validations 200
        - ask to the database if the record exist
        """
        response = self.user_signup_login()
        response = self.client.post('/rss/api/', self.data_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User_feed.objects.filter(url=self.data["url"],
                                                 author=self.userdata['username']).exists())

    def test_adding_bad_feed(self):
        """
        Test the Api for add new user's feed, end to end, using a url which 
        is not a rss source and can't be autodetect by our system.
        - post request to the API
        - serializer validation
        - status_code validations 406
        - ask to the database if the record exist
        """
        data = dict(
            title="This is a test feed",
            body="this is the body o description",
            url="https://www.youtube.com/",
        )
        response = self.user_signup_login()
        response = self.client.post('/rss/api/', data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_deleting_feed(self):
        """
        Test the Api for delete user's feeds, end to end, using
        - delete request
        - serializer validation
        - status_code validation 200
        """
        data = dict(
            id=1,
        )
        response = self.user_signup_login()
        response = self.client.post('/rss/api/',
                                    self.data,
                                    content_type='application/json')
        response = self.client.delete('/rss/api/',
                                      data=data,
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_items_from_our_feeds_first_update(self):
        """
        Test the api for get items or entries from feeds. 
        Test the entire pipeline
        - signup-login
        - post request - adding feed
        - get request - api_rss
        - validate urls
        - register error if occurs
        - Response and validata status_code 200
        - first = 1 to the first request 8 first entries
        - fiest = 0 to the next 8 entries, if they exist
        """
        response = self.user_signup_login()
        response = self.client.post('/rss/api/',
                                    self.data,
                                    content_type='application/json')
        response = self.client.post('/rss/api/update/',
                                    {"id_feed": 1, "first": 1},
                                    content_type='application/json')
        response2 = self.client.post('/rss/api/update/',
                                     {"id_feed": 1, "first": 0},
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
