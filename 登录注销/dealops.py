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

# 测试
if __name__ == '__main__':
    print '(4,10)=>', page_iter(4, 10)
    print '(1,1)=>', page_iter(1,1)
    print '(1,2)=>', page_iter(1,2)
    print '(3,5)=>', page_iter(3,5)
    print '(7,8)=>', page_iter(7,8)
    print '(8,8)=>', page_iter(8,8)



    




