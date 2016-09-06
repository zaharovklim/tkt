import requests
import json
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

from conf.settings import MAILCHIMP_API_KEY, MAILCHIMP_URL


class MailchimpRequest(object):

    def _get(uri, params):
        endpoint = urlparse.urljoin(MAILCHIMP_URL, uri)
        try:
            response = requests.get(endpoint, auth=('apikey', MAILCHIMP_API_KEY),
                                    params=params, verify=False)
        except requests.exceptions.ConnectionError as err:
            raise ValueError('Connection Error')

        if response.status_code == 200:
            response.raise_for_status()
            body = response.json()
            return body
        else:
            return Response('Invalid request', status.HTTP_400_BAD_REQUEST)

    def _post(uri, params):
        endpoint = urlparse.urljoin(MAILCHIMP_URL, uri)
        try:
            response = requests.post(endpoint, auth=('apikey', MAILCHIMP_API_KEY),
                                    data=json.dumps(params))
        except requests.exceptions.ConnectionError as err:
            raise ValueError('Connection Error')

        if response.status_code == 200:
            response.raise_for_status()
            body = response.json()
            return body
        else:
            return Response('Invalid request', status.HTTP_400_BAD_REQUEST)

    def _patch(uri, params):
        endpoint = urlparse.urljoin(MAILCHIMP_URL, uri)
        try:
            response = requests.patch(endpoint, auth=('apikey', MAILCHIMP_API_KEY),
                                    data=json.dumps(params))
        except requests.exceptions.ConnectionError as err:
            raise ValueError('Connection Error')

        if response.status_code == 200:
            response.raise_for_status()
            body = response.json()
            return body
        else:
            return Response('Invalid request', status.HTTP_400_BAD_REQUEST)

    def _delete(uri, params):
        endpoint = urlparse.urljoin(MAILCHIMP_URL, uri)
        try:
            response = requests.delete(endpoint, auth=('apikey', MAILCHIMP_API_KEY),
                                    data=json.dumps(params))
        except requests.exceptions.ConnectionError as err:
            raise ValueError('Connection Error')

        if response.status_code == 200:
            response.raise_for_status()
            body = response.json()
            return body
        else:
            return Response('Invalid request', status.HTTP_400_BAD_REQUEST)

    def process_response(self, response):
        pass #TODO


class MailchimpConstructParams(object):

    def construct_dict(params, extra_params=None):
        if extra_params is not None:
            for extra_key, extra_val in extra_params.items():
                try:
                    ext_k = extra_key.split('extra_')[1]
                except IndexError:
                    continue
                params[ext_k] = '' if ext_k not in params else params[ext_k]
                for param in extra_val:
                        params[ext_k] = '{},{}'.format(params[ext_k], param)
        return params


class MailchimpList(object):

    def get_lists(self):
        uri = 'lists'
        params = {
            'fields': 'lists.id,lists.name,lists.stats.member_count',
        }
        params = MailchimpConstructParams.construct_dict(
                            params, dict(self.GET._iterlists()))
        response = MailchimpRequest._get(uri, params)

        return response


class MailchimpSubscriber(object):

    def get_subscriber(list_id, email_md5):
        uri = 'lists/{}/members/{}'.format(list_id, email_md5)
        params = {
            'fields': 'id,email_address,status,\
                merge_fields.LNAME,merge_fields.FNAME',
        }
        response = MailchimpRequest._get(uri, params)

        return response

    def add_subscriber(self, list_id):
        uri = 'lists/{}/members/'.format(list_id)
        params = { 'email_address': self.POST['email'],
                   'merge_fields':  {
                                      'FNAME': self.POST['fname'],
                                      'LNAME': self.POST['lname']
                                    },
                   'status': 'subscribed',
                   }
        response = MailchimpRequest._post(self, uri, params)

        return response

    def update_subscriber(self, list_id, email_md5):
        uri = 'lists/{}/members/{}'.format(list_id, email_md5)
        params = dict(self.request.data._iteritems())
        response = MailchimpRequest._patch(self, uri, params)

        return response

    def retrive_list(self):
        mail_lists = MailchimpList.get_lists(self)

        if self.method == 'GET':
            list_name = self.GET.get('list_name')
        else:
            list_name = self.data['list_name']

        for mail_list in mail_lists['lists']:
            if list_name in mail_list['name']:
                list_id = mail_list['id']
        return list_id


class MailchimpCampaign(object):

    def create_campaign(self):
        uri = 'campaigns'
        params = {
            'type': self.POST['type'],
            'settings': {
                'subject_line': self.POST['subject'],
                'from_name': self.POST['from'],
                'reply_to': self.POST['reply_to'],
            }
        }
        response = MailchimpRequest._post(uri, params)

        return response

    def get_campaign(self):
        uri = 'campaigns'
        params = { 'fields': 'campaigns.id,campaigns.status,campaigns.\
                        type,campaigns.recipients,campaigns.settings' }
        response = MailchimpRequest._get(uri, params)

        return response
