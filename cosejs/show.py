#-*-coding:utf-8-*- 
from gevent import monkey;
monkey.patch_all()
from bottle import static_file
from bottle import route,run,Bottle,request,get,post,response,template,redirect

#通过定制路由将请求地址绑在回调函数上，每在浏览器上请求url，对应的回调函数运行并执行，如果没有URL绑定的回调函数则返回 404 。 路由器可以添加多个，路由添加的不是服务器上实际的物理文件，
#而是绑定到的对应的回调函数
app = Bottle()



@app.route('/<filepath:path>')
def server_static_file(filepath):
    return static_file(filepath, root='./')


@app.route('/cpcnews')
def justshow():
    return template('./index.html')

@app.route('/')
def index():
    return redirect("/cpcnews")

run(app,host='localhost',port=8080,server = 'gevent')
