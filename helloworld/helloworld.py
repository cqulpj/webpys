#coding=utf-8

import web  

urls = (  
    '/(.*)', 'hello'  
)  

render = web.template.render('templates')

class hello:  
    def GET(self, name):  
        i = web.input(times=1)  
        if not name:   
            name = 'world'  
        return 'Hello, ' + name*int(i.times) + '!'  

app = web.application(urls, globals())  

if __name__ == "__main__":  
    app.run()  
