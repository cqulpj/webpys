#coding=utf-8

import web  

urls = (  
    '/(.*)', 'hello'  
)  

render = web.template.render('')

class hello:  
    def GET(self, name):  
        return render.index()

app = web.application(urls, globals())  

if __name__ == "__main__":  
    app.run()  
