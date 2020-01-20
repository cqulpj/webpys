#coding=utf-8

# 根据当前页数cp和总页数pages生成要显示的页码序列
# 显示规则是1-1-3-1, 即：
#   1、第一页显示
#   2、当前页的前一页显示
#   3、当前页+后面两页（共三页）显示
#   4、末页显示
# 如(cp, pages)=(4, 10),生成的结果形式为[1,None,3,4,5,6,None,10]
# 其中数字为要显示的页码，None为中间省略显示的部分
def page_iter(cp, pages):
    # 输入非法则返回空序列
    if (pages<=0) or (cp<=0) or (cp>pages):
        return []

    # 首页
    ret = [1]

    # 前页
    if (cp-1) > 2:
        ret.extend([None, cp-1])
    elif (cp-1) == 2:
        ret.extend([cp-1])

    # 当前及后面两页
    se = max(2, cp)
    me = min(cp+2, pages) 
    for i in range(se, me+1):
        ret.append(i)

    # 尾页
    if pages > (me+1):
        ret.extend([None, pages])
    elif pages == (me+1):
        ret.append(pages)

    return ret

# 输入字符串的十六进制转换
# 若输入字符串中包含中文字符，也可以当作汉字内码显示函数使用
# 可选参数code指定汉字编码类型，可以为gbk、utf-8或unicode，默认为unicode
# 输出转换后的十六进制数，字节间空格隔开
# 注：要求输入参数类型为unicode
def unicode2hex(src, code='unicode'):
    # 先检测输入参数类型
    if not isinstance(src, unicode):
        return None

    # 转换编码
    if code in ['gbk', 'utf-8']:
        ss = src.encode(code)
    else:
        ss = src

    # 转换成hex形式
    sh = [hex(ord(i)).upper()[2:] for i in ss]
    return ' '.join(sh)


# 测试
if __name__ == '__main__':
    print '(4,10)=>', page_iter(4, 10)
    print '(1,1)=>', page_iter(1,1)
    print '(1,2)=>', page_iter(1,2)
    print '(3,5)=>', page_iter(3,5)
    print '(7,8)=>', page_iter(7,8)
    print '(8,8)=>', page_iter(8,8)
    print unicode2hex('hello')
    print unicode2hex(u'hello world')
    print unicode2hex(u'中国123')
    print unicode2hex(u'中国123', 'gbk')
    print unicode2hex(u'中国123', 'utf-8')
    print unicode2hex(u'百度', 'utf-8')



    




