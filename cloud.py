# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError
import json
from BookRack import *
from app import app


engine = Engine(app)


@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'

@engine.define
def searchBook(**params):
    if 'searchStr' in params :
        funResult = BookRack().searchBook(params['searchStr'],params['searchType'])
        if funResult != '101':
            resultDic = {'code':'1000','resultData':funResult}
            return json.dumps(resultDic).decode('unicode-escape')
        else:
            resultDic = {'code':'1010','resultData':funResult}
            return json.dumps(resultDic).decode('unicode-escape')
    else:
        resultDic = {'code':'1001','error':{'code':'1001','error':'传入参数错误'}}
        return json.dumps(resultDic).decode('unicode-escape')

@engine.define
def getBookInfo(**params):
    if 'bookUrl' in params:
        funResult = BookRack().getBookInfo(params['bookUrl'])
        resultDic = {'code':'1000','resultData':funResult}
        return json.dumps(resultDic).decode('unicode-escape')
    else:
        resultDic = {'code':'1001','error':{'code':'1001','error':'传入参数错误'}}
        return json.dumps(resultDic).decode('unicode-escape')

@engine.define
def getBookDirectory(**params):
    if 'directoryUrl' in params:
        funResult = BookRack().getBookDirectory(params['directoryUrl'])
        resultDic = {'code':'1000','resultData':funResult}
        return json.dumps(resultDic).decode('unicode-escape')
    else:
        resultDic = {'code':'1001','error':{'code':'1001','error':'传入参数错误'}}
        return json.dumps(resultDic).decode('unicode-escape')

@engine.define
def getBookPage(**params):
    if 'bookPageUrl' in params :
        funResult = BookRack().getBookPage(params['bookPageUrl'])
        resultDic = {'code':'1000','resultData':funResult}
        return json.dumps(resultDic).decode('unicode-escape')
    else:
        resultDic = {'code':'1001','error':{'code':'1001','error':'传入参数错误'}}
        return json.dumps(resultDic).decode('unicode-escape')

@engine.before_save('Todo')
def before_todo_save(todo):
    content = todo.get('content')
    if not content:
        raise LeanEngineError('内容不能为空')
    if len(content) >= 240:
        todo.set('content', content[:240] + ' ...')
