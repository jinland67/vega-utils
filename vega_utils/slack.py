from slack_sdk.webhook import WebhookClient
from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler

class SlackError(Exception):
    # -----------------------------------------------
    # 생성할 때 value 값을 입력 받은다.
    # -----------------------------------------------
    def __init__(self, value):
        self.value = value

    # -----------------------------------------------
    # 생성할 때 받은 value 값을 확인 한다.
    # -----------------------------------------------
    def __str__(self):
        return self.value



# ================================================================
#   [Dependancy]
#       - pip install slack_sdk
#
#   [Useage]
#       slack = Slack.send(url, message)
#
# 	[주의]
#
# ================================================================
class Slack:
    # -----------------------------------------------
    # message = [
    #   {
    #       "type": "header",
    #       "text": {
    #           "type": "plain_text",
    #           "text": "Enter the string you want to appear in the header here."
    #       }
    #   },
    #   {
    #       "type": "divider"   --> 줄바꿈을 표현하고자 할 때
    #   },
    #   {
    #       "type": "section",
    #       "text": {
    #           "type": "mrkdwn",
    #           "text": "Enter the string to be displayed in the body here."
    #       }
    #   }
    # ]
    # -----------------------------------------------
    @staticmethod
    def send(url, message):
        try:
            webhook = WebhookClient(url=url)
            rate_limit_handler = RateLimitErrorRetryHandler(max_retry_count=1)
            webhook.retry_handlers.append(rate_limit_handler)
            # message send
            response = webhook.send(
                text="fallback",
                blocks=message
            )
            # assert response.status_code == 200
            if response.status_code != 200:
                msg = 'Request to slack returned an error %s, the response is %s' % (response.status_code, response.text)
                raise SlackError(msg)
        except Exception as e:
            msg = 'Slack exception occured in send(). Message: %s' % str(e)
            raise SlackError(msg)