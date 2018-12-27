from requests import get
from lxml import etree
from copy import deepcopy
from random import choice
from execjs import compile
from json import loads



def getRes(url):
    UAlist = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    ]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': choice(UAlist)
        }
    response = get(url,headers=headers).text
    elements = etree.HTML(response)
    
    return elements

def getCVEs(year,month):
    url = 'https://nvd.nist.gov/vuln/full-listing/%d/%d'%(year,month)
    elements = getRes(url)
    CVEs = elements.xpath('//span[@class="col-md-2"]/a/@href')
    
    return CVEs

def getDetails(CVEs):
    hrefs,details = [],[]
    for CVE in CVEs:
        url = 'https://nvd.nist.gov%s'%CVE
        hrefs.append(deepcopy(url))
    for href in hrefs:
        print(href)
        elements = getRes(href)
        information = getInfor(elements)
        details.append(deepcopy(information))
    
    return details


def getInfor(elements):
    information = {}
    information['CVE-ID'] = elements.xpath('//td/div/div[2]/div/a//text()')[0]
    information['NVD 发布日期'] = elements.xpath('//td/div/div[2]/div/span[1]/text()')[0]
    information['NVD 最后修改日期'] = elements.xpath('//td/div/div[2]/div/span[2]/text()')[0]
    information['简述'] = elements.xpath('//td/div/div[1]/p[1]/text()')[0]
    if elements.xpath('//*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_Vuln3CvssPanel"]/strong/text()'):
        information['CVSS v3.0 指标'] = deepcopy(getV(3,elements))
    if elements.xpath('//*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_Vuln2CvssPanel"]/strong/text()'):
        information['CVSS v2.0 指标'] = deepcopy(getV(2,elements))
    information['参考网址'] = elements.xpath('//*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholderv_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_VulnHyperlinksPanel"]/table/tbody//a/@href')
    if elements.xpath('//*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_VulnTechnicalDetailsDiv"]/ul/li/text()'):
        tmp1 = elements.xpath('//*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_VulnTechnicalDetailsDiv"]/ul/li/text()[1]')[0]
        tmp2 = elements.xpath('//*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_VulnTechnicalDetailsDiv"]/ul/li/a/text()')[0]
        tmp3 = elements.xpath('//*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_VulnTechnicalDetailsDiv"]/ul/li/text()[2]')[0]
        information['漏洞类型'] = ''.join([trans(tmp1),tmp2,tmp3])
    if elements.xpath('//*[@id="VulnChangeHistorySection"]/text()'):
        information['更新记录'] = elements.xpath('//*[@id="p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_VulnChangeHistoryDiv"]/small/text()')[0][1:-3].strip()

    return information


def getV(version,elements):
    impact = {}
    if version == 3:
        div = 'p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_Vuln3CvssPanel'
    else:
        div = 'p_lt_WebPartZone1_zoneCenter_pageplaceholder_p_lt_WebPartZone1_zoneCenter_VulnerabilityDetail_VulnFormView_Vuln2CvssPanel'

    impact['基本分数'] = ' '.join(elements.xpath('//div[@id="{}"]/p/a/span/text()'.format(div)))
    impact['影响分数'] = elements.xpath('//div[@id="{}"]/p[1]/span[2]/text()'.format(div))[0].strip()
    impact['可利用性分数'] = elements.xpath('//div[@id="{}"]/p[1]/span[3]/text()'.format(div))[0].strip()
    impact['攻击方向'] = elements.xpath('//div[@id="{}"]/p[2]/span[1]/text()'.format(div))[0].strip()
    impact['攻击复杂度'] = elements.xpath('//div[@id="{}"]/p[2]/span[2]/text()'.format(div))[0].strip()

    if version ==3:
        impact['权限'] = elements.xpath('//div[@id="{}"]/p[2]/span[3]/text()'.format(div))[0].strip()
        impact['用户交互'] = elements.xpath('//div[@id="{}"]/p[2]/span[4]/text()'.format(div))[0].strip()
        impact['范围'] = elements.xpath('//div[@id="{}"]/p[2]/span[5]/text()'.format(div))[0].strip()
        impact['机密性'] = elements.xpath('//div[@id="{}"]/p[2]/span[6]/text()'.format(div))[0].strip()
        impact['完整性'] = elements.xpath('//div[@id="{}"]/p[2]/span[7]/text()'.format(div))[0].strip()
        impact['可用性'] = elements.xpath('//div[@id="{}"]/p[2]/span[8]/text()'.format(div))[0].strip()
    else:
        impact['身份验证'] = elements.xpath('//div[@id="{}"]/p[2]/span[3]/text()'.format(div))[0].strip()
        impact['机密性'] = elements.xpath('//div[@id="{}"]/p[2]/span[4]/text()'.format(div))[0].strip()
        impact['完整性'] = elements.xpath('//div[@id="{}"]/p[2]/span[5]/text()'.format(div))[0].strip()
        impact['可用性'] = elements.xpath('//div[@id="{}"]/p[2]/span[6]/text()'.format(div))[0].strip()
        impact['附加信息'] = elements.xpath('//div[@id="{}"]/p[2]/span[7]/text()'.format(div))[0].strip()
    
    return impact


class Py4Js():
    
    def __init__(self):
        self.ctx = compile(""" 
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
        r=get(url)
        result=loads(r.text)
        if result[7]!=None:
        # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
            try:
                correctText=result[7][0].replace('<b><i>',' ').replace('</i></b>','')
                print(correctText)
                correctUrl=buildUrl(correctText,js.getTk(correctText))
                correctR=get(correctUrl)
                newResult=loads(correctR.text)
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

def trans(x):
    sen = []
    result = translate(x)
    for res in result:
        if res[0] is not None:
            sen.append(res[0])
    str = ''.join(sen)
    return str