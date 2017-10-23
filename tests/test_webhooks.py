from semantics3 import Semantics3Request
import unittest
from os import environ

sem3 = Semantics3Request(
        api_key = environ["SEM3_API_KEY"],
        api_secret = environ["SEM3_API_SECRET"]
        )


class TestWebhoOKsAPI(unittest.TestCase):

    """Docstring for TestWebhoOKs. """

    def test_webhook_registration(self):
        """@todo: Docstring for test_webhook_registration.

        :returns: @todo
        """
        result = sem3.run_query('webhooks', "POST", {"webhook_uri" : "https://semantics3-basic-webhook-receiver-11ozacc07xtw.runkit.sh/"})
        self.assertIn('created', result["results"])

    def test_get_webhooks(self):
        """@todo: Docstring for test_get_webhooks.
        :returns: @todo

        """
        webhooks = sem3.run_query('webhooks', "GET")
        self.assertEqual(webhooks['code'], 'OK')

    def test_register_event(self):
        """@todo: Docstring for function.

        :returns: @todo

        """
        webhooks = sem3.run_query('webhooks', "GET")
        if len(webhooks['results']):
            webhook_id = webhooks['data'][0]['id']
            params = {
                    "type": "price.change",
                    "product": {
                        "sem3_id": "1QZC8wchX62eCYS2CACmka"
                        },
                    "constraints" : {
                        "gte" : 10,
                        "lte" : 100
                        }
                    }
            response = sem3.run_query('webhooks/%s/events' % webhook_id, "POST", params)
            self.assertEqual(response['code'], 'OK')
            del params['constraints']
            response1 = sem3.run_query('webhooks/%s/events' % webhook_id, "POST", params)
            self.assertEqual(response1['code'], 'OK')
        else:
            self.assertEqual(webhooks['code'], 'OK')

    def test_delete_webhook(self):
        """@todo: Docstring for test_delete_webhook.
        :returns: @todo

        """
        webhooks = sem3.run_query('webhooks', "GET")
        if len(webhooks['results']):
            webhook_id = webhooks['results'][0]['id']
            response = sem3.run_query('webhooks/%s' % webhook_id, "DELETE")
            self.assertEqual(response['code'], 'OK')
        else:
            self.assertEqual(webhooks['code'], 'OK')
