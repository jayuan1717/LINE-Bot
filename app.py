from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('DQNyq9vz1k3BHJAaGMyypvtrx+wjyXFODpdiPSiK4WvBRqJL9IHfZLfVd6s6Q6MngDSIYIRkItmlOqLkKvdrS+HcdNyjX+vHskxVYB++4LeoNUFQZoKaempvdMMTSZXI6SlCAnOKC4YJn+/xFId5tQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('df20b85f3ce5b34753fae6a15f35dc34')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()