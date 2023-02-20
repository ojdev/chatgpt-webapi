import os
import flask,json
from flask import request
from revChatGPT.V1 import Chatbot
from gevent import pywsgi

access_token = os.environ.get("access_token", "")

config={
  "access_token": access_token
}

# 创建一个服务，把当前这个python文件当做一个服务
app = flask.Flask(__name__)
chatbot = Chatbot(config)
def chat(prompt,conversation_id=None,parent_id=None):
  message = ""
  for data in chatbot.ask(
    prompt,
    conversation_id = conversation_id,
    parent_id = parent_id,
    gen_title = True
  ):
    parent_id = data["parent_id"]
    conversation_id = data["conversation_id"]
    message = data["message"]
  response={
    "message": message,
    "parent_id": parent_id,
    "conversation_id": conversation_id
  }
  return response
@app.route('/ask', methods=['post'])
def chatapi():
    requestJson = request.get_data()
    if requestJson is None or requestJson == "" or requestJson == {}:
        resu = {'code': 1, 'msg': '请求内容不能为空'}
        return json.dumps(resu, ensure_ascii=False)
    data = json.loads(requestJson)
    if ( 'conversation_id' in data) == False:
      data['conversation_id']=None
    if ( 'parent_id' in data) == False:
      data['parent_id']=None
    try:
        msg = chat(data['msg'])
    except Exception as error:
        print("接口报错")
        resu = {'code': 1, 'msg': '请求异常: ' + str(error)}
        return json.dumps(resu, ensure_ascii=False)
    else:
        resu = {'code': 0, 'data': msg}
        return json.dumps(resu, ensure_ascii=False)

@app.route('/conversation/<uuid:convo_id>/delete', methods=['post'])
def delete_conversation(convo_id):
    chatbot.delete_conversation(convo_id)
    resu = {'code': 0, 'msg': '删除成功: ' }
    return json.dumps(resu, ensure_ascii=False)
if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    server.serve_forever()
