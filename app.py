import flask
from flask import Flask, request
from werkzeug.utils import secure_filename, escape
import os
import json

import toNet.net

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
RADIO_ALLOWED_EXTENSIONS = set(['pcm', 'wav', 'amr', 'opus', 'mp3'])
YOUR_RADIO_ALLOWED_EXTENSIONS = set(['pcm', 'mp3'])
PIC_ALLOWED_EXTENSIONS = set(['png', 'jpg'])


# 用于判断音频文件后缀
def radio_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in RADIO_ALLOWED_EXTENSIONS


# 用于判断图片文件后缀
def pic_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in PIC_ALLOWED_EXTENSIONS


def your_radio_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in YOUR_RADIO_ALLOWED_EXTENSIONS


# -----------------------------------------------------------------------------------------------

@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/r2t')
def h_r2t():
    return flask.render_template('r2t.html')


@app.route('/p2t')
def h_p2t():
    return flask.render_template('p2t.html')


@app.route('/flower')
def self():
    return flask.render_template('flower.html')


@app.route('/star')
def your():
    return flask.render_template('star.html')


@app.route('/upload')
def upload():
    return flask.render_template('upload.html')


# -----------------------------------------------------------------------------------------------


@app.route('/radio2text', methods=["POST"])
def radio2text():
    print("------------------------------------------------------------------------")
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and radio_allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        f_name = secure_filename(f.filename)
        print(f_name)
        ext = f_name.rsplit('.', 1)[1]  # 获取文件后缀
        new_filename = "local_data" + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        print(file_dir + new_filename)
        text = toNet.net.r2t(file_dir + "/" + new_filename, ext)
        if toNet.net.ok_text(text):
            result = {"status": False, "msg": "识别文字种含有敏感词"}
            json_Msg = json.dumps(result, ensure_ascii=False)
            return json_Msg
        result = {"status": True, "msg": text}
        json_Msg = json.dumps(result, ensure_ascii=False)
        return json_Msg
    result = {"status": True, "msg": "该格式暂不支持访问"}
    json_Msg = json.dumps(result, ensure_ascii=False)
    return json_Msg


@app.route('/proto2text', methods=["POST"])
def proto2text():
    print("------------------------------------------------------------------------")
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and pic_allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        f_name = secure_filename(f.filename)
        print(f_name)
        ext = f_name.rsplit('.', 1)[1]  # 获取文件后缀
        new_filename = "local_data" + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        print(file_dir + "/" + new_filename)
        text = toNet.net.p2t(file_dir + "/" + new_filename)
        print(text)
        if toNet.net.ok_text(text):
            result = {"status": False, "msg": "识别文字种含有敏感词"}
            json_Msg = json.dumps(result, ensure_ascii=False)
            return json_Msg
        result = {"status": True, "msg": text}
        json_Msg = json.dumps(result, ensure_ascii=False)
        return json_Msg
    result = {"status": True, "msg": "该格式暂不支持访问"}
    json_Msg = json.dumps(result, ensure_ascii=False)
    return json_Msg



@app.route('/select_flower', methods=["POST"])
def select_flower():
    print("------------------------------------------------------------------------")
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and pic_allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        f_name = secure_filename(f.filename)
        print(f_name)
        ext = f_name.rsplit('.', 1)[1]  # 获取文件后缀
        new_filename = "local_data" + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        print(file_dir + "/" + new_filename)
        return toNet.net.flower(file_dir + "/" + new_filename,ext)
    result = {"status": True, "msg": "该格式暂不支持访问"}
    json_Msg = json.dumps(result, ensure_ascii=False)
    return json_Msg



@app.route('/select_star', methods=["POST"])
def select_star():
    print("------------------------------------------------------------------------")
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and pic_allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        f_name = secure_filename(f.filename)
        print(f_name)
        ext = f_name.rsplit('.', 1)[1]  # 获取文件后缀
        new_filename = "local_data" + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        print(file_dir + "/" + new_filename)
        return toNet.net.star(file_dir + "/" + new_filename,ext)
    result = {"status": True, "msg": "该格式暂不支持访问"}
    json_Msg = json.dumps(result, ensure_ascii=False)
    return json_Msg


@app.route('/your_radio', methods=["POST"])
def your_radio():
    print("------------------------------------------------------------------------")
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and your_radio_allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        f_name = secure_filename(f.filename)
        ext = f_name.rsplit('.', 1)[1]  # 获取文件后缀
        new_filename = "local_data" + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        print(file_dir + new_filename)
        text = request.form.get('my_text')
        json_Msg = toNet.net.your(file_dir + "/" + new_filename, text, ext)
        return json_Msg
    result = {"status": True, "msg": "该格式暂不支持访问"}
    json_Msg = json.dumps(result, ensure_ascii=False)
    return json_Msg


@app.route('/self_radio', methods=["POST"])
def self_radio():
    print("------------------------------------------------------------------------")
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and your_radio_allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        f_name = secure_filename(f.filename)
        ext = f_name.rsplit('.', 1)[1]  # 获取文件后缀
        new_filename = "local_data" + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        print(file_dir + new_filename)
        text = request.form.get('my_text')
        json_Msg = toNet.net.self(file_dir + "/" + new_filename, text, ext)
        return json_Msg
    result = {"status": True, "msg": "该格式暂不支持访问"}
    json_Msg = json.dumps(result, ensure_ascii=False)
    return json_Msg


if __name__ == '__main__':
    app.run()
