# coding=utf-8

from Aum_water.start import app
from flask import make_response, url_for, request, jsonify, abort
from flask import session
from flask import redirect


# cookie设置并且获取
@app.route("/cookie")
def set_cookie():
    """
    
    :return: 
    """
    resp = make_response('this is to set cookie')
    resp.set_cookie('username', 'sun')
    return resp


@app.route("/request")
def resp_cookie():
    """
    
    :return: 
    """
    resp = request.cookies.get("username")
    return resp


# session状态保持
@app.route("/session")
def set_session():
    """
    
    :return: 
    """
    session['username'] = "moon"
    return redirect(url_for("get_session"))


@app.route("/get_session")
def get_session():
    """
    
    :return: 
    """
    return session.get("username")


@app.route("/", methods=["POST"])
def hello():
    """
    
    :return: 
    """
    pic = request.files.get("pic")
    pic.save("./static/aaa.png")
    return "hello world! and redirect"


# 路由传参
@app.route('/user/<re("[0-9]{3}"):user_id>')
def user_info(user_id):
    """
    
    :param user_id: 
    :return: 
    """
    return "hello %s" % user_id


# 指定请求方式
@app.route("/demo", methods=["GET", "POST"])
def demo():
    """
    
    :return: 
    """
    return request.method


# 返回json数据
@app.route("/json")
def return_json():
    """
    
    :return: 
    """
    json_dict = {
        "uid": 10,
        "user_name": "laowang"
    }
    return jsonify(json_dict)


# 重定向
@app.route("/redirect")
def redirect_demo():
    """
    
    :return: 
    """
    # return redirect(url_for("user_info",user_id=100))
    return redirect(url_for('user_info', user_id=100))


@app.route("/status_code")
def status_code():
    """
    
    :return: 
    """
    abort(400)

    return "状态码 666"


# 错误捕获
@app.errorhandler(400)
def internal_server_error():
    """
    
    :param : 
    :return: 
    """
    return "主动抛出400错误"
