# coding: UTF-8

import os,sys
import json
from flask import Flask, render_template, url_for, request, jsonify
from flask import *
import argparse
import logging, logging.config, yaml
import time
from utils.calSparkAPI import *
import os
##########################################
## Options and defaults
##########################################
def getOptions():
    parser = argparse.ArgumentParser(description='python *.py [option]')
    parser.add_argument('--ip', dest='ip', help="ip", default='0.0.0.0')
    parser.add_argument('--port', dest='port', help="port", default=8080)
    parser.add_argument('--debug', dest='debug', help="if debug", default='True')
    args = parser.parse_args()

    return args


"""
Flask
"""
app = Flask(__name__,static_folder='static',template_folder='static/html')
"""
log
"""
logging.config.dictConfig(yaml.load(open(os.path.join(sys.path[0], 'logging.conf')),Loader=yaml.FullLoader))
logger = logging.getLogger()


def generate_caption(image):
    input_prompt = """
    你是一个营养专家，根据给出的图片，请分析其中的食物，给出详细的营养和卡路里分析。输出格式为：

    面条 - 包含多少卡路里，有什么营养成分
    虾 - 包含多少卡路里，有什么营养成分
    一共多少卡路里热量。

    最后，评估作为一顿正餐，是否营养均衡，给出改善建议。
    """
    ans = calsparkapi(image, input_prompt)
    return ans

@app.route('/' , methods=['GET'])
def homepage():
    return render_template(r"homepage.html")

@app.route('/certificates' , methods=['GET'])
def certificates():
    return render_template(r"certificates.html")

@app.route('/aboutme' , methods=['GET'])
def aboutme():
    return render_template(r"aboutme.html")

@app.route('/picbatch' , methods=['GET'])
def picshow():
    item = request.args.get('item', 'chuanchuan1')
    path_all = os.path.join(r"static/images/ppt",item)
    flist = os.listdir(path_all)
    flist = sorted(flist)
    return render_template(r"picbatch.html",images=flist,item=item)

@app.route('/calorie_spark' , methods=['POST'])
def calorie_spark():
    st = time.time()
    # 解析请求
    requestjson = request.get_json(force=True, silent=True)
    logger.info(requestjson)

    imagedata = requestjson["image"]
    pred = generate_caption(imagedata)

    result = {'msg': "success",
              'status': 0,
              'prediction': str(pred),
              "time_used":time.time()-st}
    logger.info(result)

    resultstr = json.dumps(result, ensure_ascii=False)
    logger.debug("response:" + resultstr)
    return resultstr


if __name__ == "__main__":
    options = getOptions()
    print(options)
    check = {"False":False,"True":True}
    app.run(host=options.ip, port=options.port,debug=check[options.debug])
