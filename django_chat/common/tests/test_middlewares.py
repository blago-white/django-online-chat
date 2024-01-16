from typing import Any

from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory

from common import tests_utils
from .. import middlewares


class UserLoggedInMiddlewareTestCase(TestCase):
    _middleware_instance: middlewares.UserLoggedInMiddleware
    _request_factory: RequestFactory
    _test_user: User

    _TEST_VIEW_RESPONSE: str = "View response"

    def setUp(self) -> None:
        self._middleware_instance = middlewares.UserLoggedInMiddleware(get_response=lambda _: self._TEST_VIEW_RESPONSE)
        self._request_factory = RequestFactory()
        self._test_user = tests_utils.get_test_user()

    def test_call(self):
        self.assertEqual(
            self._run_request_through_middleware(path="/chat/").__class__,
            HttpResponseRedirect
        )

        self.assertEqual(
            self._run_request_through_middleware(path="/admin/", request_user=self._test_user),
            self._TEST_VIEW_RESPONSE
        )

        self.assertEqual(
            self._run_request_through_middleware(path="/chat/", request_user=self._test_user),
            self._TEST_VIEW_RESPONSE
        )

        self.assertEqual(
            self._run_request_through_middleware(path="/", request_user=self._test_user).__class__,
            HttpResponseRedirect
        )

    def _run_request_through_middleware(self, path: str, request_user: User = None) -> Any:
        test_request = self._request_factory.get(path=path)

        if request_user.__class__ is User:
            test_request.user = request_user

        return self._middleware_instance(request=test_request)
