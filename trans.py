import requests
import json
import execjs


class Py4Js():
    
    def __init__(self):
        self.ctx = execjs.compile(""" 
    function TL(a) { 
    var k = ""; 
    var b = 406644; 
    var b1 = 3293161072;       
    var jd = "."; 
    var $b = "+-a^+6"; 
    var Zb = "+-3^+b+-f";    
    for (var e = [], f = 0, g = 0; g < a.length; g++) { 
        var m = a.charCodeAt(g); 
        128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
        e[f++] = m >> 18 | 240, 
        e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
        e[f++] = m >> 6 & 63 | 128), 
        e[f++] = m & 63 | 128) 
    } 
    a = b; 
    for (f = 0; f < e.length; f++) a += e[f], 
    a = RL(a, $b); 
    a = RL(a, Zb); 
    a ^= b1 || 0; 
    0 > a && (a = (a & 2147483647) + 2147483648); 
    a %= 1E6; 
    return a.toString() + jd + (a ^ b) 
  };      
  function RL(a, b) { 
    var t = "a"; 
    var Yb = "+"; 
    for (var c = 0; c < b.length - 2; c += 3) { 
        var d = b.charAt(c + 2), 
        d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
        d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
        a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
    } 
    return a 
  } 
 """)
    def getTk(self,text):  
        return self.ctx.call("TL",text)
def buildUrl(text,tk):
    baseUrl='https://translate.google.cn/translate_a/single'
    baseUrl+='?client=t&'
    baseUrl+='s1=auto&'
    baseUrl+='t1=zh-CN&'
    baseUrl+='h1=zh-CN&'
    baseUrl+='dt=at&'
    baseUrl+='dt=bd&'
    baseUrl+='dt=ex&'
    baseUrl+='dt=ld&'
    baseUrl+='dt=md&'
    baseUrl+='dt=qca&'
    baseUrl+='dt=rw&'
    baseUrl+='dt=rm&'
    baseUrl+='dt=ss&'
    baseUrl+='dt=t&'
    baseUrl+='ie=UTF-8&'
    baseUrl+='oe=UTF-8&'
    baseUrl+='otf=1&'
    baseUrl+='pc=1&'
    baseUrl+='ssel=0&'
    baseUrl+='tsel=0&'
    baseUrl+='kc=2&'
    baseUrl+='tk='+str(tk)+'&'
    baseUrl+='q='+text
    return baseUrl
def translate(text):
    url=buildUrl(text,js.getTk(text))
    res=''
    try:
        r=requests.get(url)
        result=json.loads(r.text)
        if result[7]!=None:
        # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
            try:
                correctText=result[7][0].replace('<b><i>',' ').replace('</i></b>','')
                print(correctText)
                correctUrl=buildUrl(correctText,js.getTk(correctText))
                correctR=requests.get(correctUrl)
                newResult=json.loads(correctR.text)
                res=newResult[0][0][0]
            except Exception as e:
                print(e)
                res=result[0][0][0]
        else:
            res=result[0]
    except Exception as e:
        res=''
        print(url)
        print("翻译"+text+"失败")
        print("错误信息:")
        print(e)
    finally:
        return res

js=Py4Js()

def trans():
    sen = []
    result = translate('By selecting these links you will be leaving NIST webspace. We have provided these links to other web sites because they may have information that would be of interest to you. No inferences should be drawn on account of other sites being referenced, or not, from this page. There may be other web sites that are more appropriate for your purpose. NIST does not necessarily endorse the views expressed, or concur with the facts presented on these sites. Further, NIST does not endorse any commercial products that may be mentioned on these sites. Please address comments about this page to')
    for res in result:
        if res[0] is not None:
            sen.append(res[0])
    str = ''.join(sen)
    return str

trans()