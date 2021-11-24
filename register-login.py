from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from setToken import generate_token

app = Flask(__name__)

# 配置数据库地址
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost:3306/flask_sql'
# mysql://用户名:密码@主机名/ip地址:端口号/数据库名

# 创建数据库对象
db = SQLAlchemy(app)


class User(db.Model):
    # 定义表名
    __tablename__ = 'User'
    # 定义字段
    userName = db.Column(db.Text, primary_key=True)
    passWord = db.Column(db.Text)


# 注册
@app.route("/register/", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    save = User(userName=username, passWord=password)
    # 添加数据
    db.session.add(save)
    # 提交修改
    db.session.commit()
    return jsonify(msg="注册成功")


# 登录
@app.route("/login/", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    obj = User.query.filter_by(userName=username).first()
    if not obj:
        return jsonify(msg="账号不存在")
    if obj.passWord == password:
        token = generate_token(username)
        return jsonify({'token': token, "msg": "登录成功"})
        # return jsonify(msg="登录成功")
    else:
        return jsonify(msg="密码错误")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
