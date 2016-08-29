from semantics3 import Products
import unittest

sem3 = Products(
        api_key = "",
        api_secret = ""
        )


class TestWebhooksAPI(unittest.TestCase):

    """Docstring for TestWebhooks. """

    def test_webhook_registration(self):
        """@todo: Docstring for test_webhook_registration.

        :returns: @todo
        """
        result = sem3.run_query('webhooks', "POST", {"webhook_uri" : "https://sem3-webhooks-verification.ngrok.io"})
        self.assertIn('created', result)
    
    def test_get_webhooks(self):
        """@todo: Docstring for test_get_webhooks.
        :returns: @todo

        """
        webhooks = sem3.run_query('webhooks', "GET")
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
