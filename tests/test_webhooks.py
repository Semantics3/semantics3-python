from semantics3 import Semantics3Request
import unittest
from os import environ

sem3 = Semantics3Request(
        api_key = environ["SEM3_API_KEY"],
        api_secret = environ["SEM3_API_SECRET"]
        )


class TestWebhooksAPI(unittest.TestCase):

    """Docstring for TestWebhooks. """

    def test_webhook_registration(self):
        """@todo: Docstring for test_webhook_registration.

        :returns: @todo
        """
        result = sem3.run_query('webhooks', "POST", {"webhook_uri" : "http://decce40a.ngrok.io"})
        self.assertIn('created', result)
    
    def test_get_webhooks(self):
        """@todo: Docstring for test_get_webhooks.
        :returns: @todo

        """
        webhooks = sem3.run_query('webhooks', "GET")
        self.assertEqual(webhooks['status'], 'ok')

    def test_register_event(self):
        """@todo: Docstring for function.

        :returns: @todo

        """
        webhooks = sem3.run_query('webhooks', "GET")
        if len(webhooks['data']):
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
            self.assertEqual(response['status'], 'ok')
            del params['constraints']
            response1 = sem3.run_query('webhooks/%s/events' % webhook_id, "POST", params)
            self.assertEqual(response1['status'], 'ok')
        else:
            self.assertEqual(webhooks['status'], 'ok')
    
    def test_delete_webhook(self):
        """@todo: Docstring for test_delete_webhook.
        :returns: @todo

        """
        webhooks = sem3.run_query('webhooks', "GET")
        if len(webhooks['data']):
            webhook_id = webhooks['data'][0]['id']
            response = sem3.run_query('webhooks/%s' % webhook_id, "DELETE")
            self.assertEqual(response['status'], 'ok')
        else:
            self.assertEqual(webhooks['status'], 'ok')
