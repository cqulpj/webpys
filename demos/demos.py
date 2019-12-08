#coding=utf-8

import web  
from web.contrib.template import render_jinja

urls = (  
    '/hello', 'hello',
    '/ctx', 'ctx'
)  

render = render_jinja('', encoding='utf-8',)

# 添加请求前的钩子函数
def my_loadhook():
    print('my load hook')

# 添加请求后的钩子函数
def my_unloadhook():
    print('my unload hook')

class hello:  
    def GET(self):  
        return render.jinja_index(name=u'张三', 
                date=u'2019-12-06 15:21', 
                addr=u'中国')

class ctx:
    def GET(self):
        return str(web.ctx)

app = web.application(urls, globals())  
app.add_processor(web.loadhook(my_loadhook))
app.add_processor(web.unloadhook(my_unloadhook))

if __name__ == "__main__":  
    app.run()  
