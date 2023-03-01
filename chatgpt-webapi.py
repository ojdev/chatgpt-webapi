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

# 对话
@app.route('/ask', methods=['post'])
def chatapi():
    requestJson = request.get_data()
    if requestJson is None or requestJson == "" or requestJson == {}:
        resu = {'code': 1, 'msg': '请求内容不能为空'}
        return json.dumps(resu, ensure_ascii=False)
    data = json.loads(requestJson)
    if ('conversation_id' in data) == False:
        data['conversation_id'] = None
    if ('parent_id' in data) == False:
        data['parent_id'] = None
    try:
        if data['conversation_id'] is None and data['parent_id'] is None:
            chatbot.reset_chat()
        for i in chatbot.ask(
            data['msg'],
            data['conversation_id'],
            data['parent_id']
        ):
            result = i
    except Exception as error:
        print("接口报错")
        return json.dumps({'code': 1, 'msg': '请求异常: ' + str(error)}, ensure_ascii=False)
    else:
        return json.dumps({'code': 0, 'data': result}, ensure_ascii=False)

# 由于逆向工程的接口原因，参数传递都是正确的，但是始终返回的都是所有对话
@app.route('/conversations', methods=['get'])
def get_conversations():
    return json.dumps(chatbot.get_conversations(offset=0, limit=100, encoding='utf-8'), ensure_ascii=False)
  
# 获取历史对话
@app.route('/conversation/<uuid:convo_id>', methods=['get'])
def get_msg_history(convo_id):
    return json.dumps(chatbot.get_msg_history(convo_id, encoding='utf-8'), ensure_ascii=False)
  
# 修改对话标题
@app.route('/conversation/<uuid:convo_id>/title', methods=['post'])
def change_title(convo_id):
    requestJson = request.get_data()
    data = json.loads(requestJson)
    chatbot.change_title(convo_id, data['title'])   
    return json.dumps({'code': 0, 'msg': '成功: ' }, ensure_ascii=False)
  
# 删除对话
@app.route('/conversation/<uuid:convo_id>/delete', methods=['post'])
def delete_conversation(convo_id):
    chatbot.delete_conversation(convo_id)
    return json.dumps({'code': 0, 'msg': '成功: ' }, ensure_ascii=False)

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    server.serve_forever()
