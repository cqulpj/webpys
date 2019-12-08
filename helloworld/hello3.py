#coding=utf-8

import web  
from web.contrib.template import render_jinja

urls = (  
    '/(.*)', 'hello'  
)  

render = render_jinja('', encoding='utf-8',)

class hello:  
    def GET(self, name):  
        return render.jinja_index(name=u'张三', 
                date=u'2019-12-06 15:21', 
                addr=u'中国')

app = web.application(urls, globals())  

if __name__ == "__main__":  
    app.run()  
