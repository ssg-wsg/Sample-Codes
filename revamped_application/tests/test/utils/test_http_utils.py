import unittest

from revamped_application.utils.http_utils import *


class TestHttpUtils(unittest.TestCase):
    """
    Tests all the methods and classes within the http_utils file.
    """

    def test_with_endpoint(self):
        builder1 = HTTPRequestBuilder().with_endpoint("http://localhost:8080")
        builder2 = HTTPRequestBuilder().with_endpoint("http://localhost:8080/",
                                                      direct_argument="direct_argument")
        builder3 = HTTPRequestBuilder().with_endpoint("http://localhost:8080",
                                                      direct_argument="direct_argument/")
        builder4 = HTTPRequestBuilder().with_endpoint("http://localhost:8080/",
                                                      direct_argument="direct_argument/arg1/arg2/arg3")

        self.assertEqual(builder1.endpoint, "http://localhost:8080")
        self.assertEqual(builder2.endpoint, "http://localhost:8080/direct_argument")
        self.assertEqual(builder3.endpoint, "http://localhost:8080/direct_argument")
        self.assertEqual(builder4.endpoint, "http://localhost:8080/direct_argument/arg1/arg2/arg3")

    def test_with_header(self):
        with self.assertRaises(ValueError):
            HTTPRequestBuilder().with_header(None, "value")

        with self.assertRaises(ValueError):
            HTTPRequestBuilder().with_header("key", None)

        with self.assertRaises(ValueError):
            HTTPRequestBuilder().with_header("", "value")

        builder = HTTPRequestBuilder().with_header("key", "value")
        self.assertEqual(builder.header, {"accept": "application/json", "key": "value"})

    def test_with_param(self):
        with self.assertRaises(ValueError):
            HTTPRequestBuilder().with_param(None, "value")

        with self.assertRaises(ValueError):
            HTTPRequestBuilder().with_param("", "value")

        with self.assertRaises(ValueError):
            HTTPRequestBuilder().with_param("key", lambda x: 1)

        builder = HTTPRequestBuilder().with_param("key", "value")
        self.assertEqual(builder.params, {"key": "value"})

    def test_with_body(self):
        with self.assertRaises(ValueError):
            HTTPRequestBuilder().with_body(None)

        with self.assertRaises(ValueError):
            HTTPRequestBuilder().with_body("")

        builder = HTTPRequestBuilder().with_body({"data": "value"})
        self.assertEqual(builder.body, json.dumps({"data": "value"}))

    def test_with_api_version(self):
        with self.assertRaises(ValueError):
            HTTPRequestBuilder().with_api_version(None)

        with self.assertRaises(ValueError):
            HTTPRequestBuilder().with_api_version(1)

        builder = HTTPRequestBuilder().with_api_version("v1")
        self.assertEqual(builder.header, {"accept": "application/json", "x-api-version": "v1"})

    def test_get(self):
        builder = HTTPRequestBuilder()

        with self.assertRaises(ValueError):
            builder.get()

    def test_post(self):
        builder = HTTPRequestBuilder()

        with self.assertRaises(ValueError):
            builder.post()

    def test_post_encrypted(self):
        builder = HTTPRequestBuilder()

        with self.assertRaises(ValueError):
            builder.post_encrypted()

    def test_repr(self):
        post1 = "POST None\n\nHeaders\n-------\naccept: application/json\n\nBody\n-------\n{}\n"
        post2 = ("POST https://www.google.com?param=value\n\nHeaders\n-------\naccept: application/json\nheader: "
                 "value\n\nBody\n-------\n{\n    \"data\": \"value\"\n}\n")
        get1 = "GET None\n\nHeaders\n-------\naccept: application/json\n\nBody\n-------\n{}\n"
        get2 = ("GET https://www.google.com?param=value\n\nHeaders\n-------\naccept: application/json\nheader: "
                "value\n\nBody\n-------\n{\n    \"data\": \"value\"\n}\n")

        self.assertEqual(HTTPRequestBuilder().repr(HttpMethod.POST), post1)
        self.assertEqual(HTTPRequestBuilder()
                         .with_header("header", "value")
                         .with_param("param", "value")
                         .with_endpoint("https://www.google.com/")
                         .with_body({"data": "value"})
                         .repr(HttpMethod.POST), post2)

        self.assertEqual(HTTPRequestBuilder().repr(HttpMethod.GET), get1)
        self.assertEqual(HTTPRequestBuilder()
                         .with_header("header", "value")
                         .with_param("param", "value")
                         .with_endpoint("https://www.google.com/")
                         .with_body({"data": "value"})
                         .repr(HttpMethod.GET), get2)
