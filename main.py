import fun

def write(details,year,month):
    fileName = 'CVE_%d_%d'%(year,month)
    with open(fileName,'w') as f:
        for detail in details:
            for key,value in detail.items():
                if key == 'CVSS v2.0 指标' or key == 'CVSS v3.0 指标':
                    f.writelines(['\r\n',key,':','\r\n'])
                    for ke,va in value.items():
                        if ke == '附加信息':
                            f.writelines([ke,':\t',fun.trans(va),'\r\n'])
                        else:
                            f.writelines([ke,':\t',va,'\r\n'])
                    f.writelines(['\r\n'])
                elif key == '参考网址':
                    f.writelines([key,':','\r\n'])
                    for href in value:
                        f.writelines([href,'\r\n'])
                elif key == 'CVE-ID' or key == '漏洞类型':
                    print(key,':\t',value,'\r\n')
                    f.writelines([key,':\t',value,'\r\n'])
                else:
                    f.writelines([key,':\t',fun.trans(value),'\r\n'])
            f.writelines(['='*50,'\r\n'])
    f.closed


def show(details):
    for detail in details:
        for key,value in detail.items():
            if key == 'CVSS v2.0 指标' or key == 'CVSS v3.0 指标':
                print('\n',key,':')
                for ke,va in value.items():
                    if ke == '附加信息':
                        print(ke,':\t',fun.trans(va))
                    else:
                        print(ke,':\t',va)
                print('\n')
            elif key == '参考网址':
                print(key,':')
                for href in value:
                    print(href)
            elif key == 'CVE-ID' or key == '漏洞类型':
                print(key,':\t',value)
            else:
                print(key,':\t',fun.trans(value))
        print('='*50)

def main():
    while 1:
        year = int(input("你想爬哪年的CVE?(1988-2018)"))
        if year >= 1988 and year <= 2018:
            break
        else:
            print("请重新输入")
    while 1:
        month = int(input("你想爬哪年的CVE?(1-12)"))
        if month >= 1 and month <= 12:
            break
        else:
            print("请重新输入")
    while 1:
        mod = int(input("是否保存数据到本地?\n1 保存\n2 不保存"))
        if mod == 1 or mod == 2:
            break
        else:
            print("请重新输入")
    CVEs = fun.getCVEs(year,month)
    details = fun.getDetails(CVEs)
    if mod == 1:
        write(details,year,month)
    else:
        show(details)
    

if __name__ == "__main__":
    main()



'''
    for detail in details:
        for key,value in detail.items():
            if key == 'CVSS v2.0 指标' or key == 'CVSS v3.0 指标':
                print('\n',key,':')
                for ke,va in value.items():
                    if ke == '附加信息':
                        print(ke,':\t',fun.trans(va))
                    else:
                        print(ke,':\t',va)
                print('\n')
            elif key == '参考网址':
                print(key,':')
                for href in value:
                    print(href)
            elif key == 'CVE-ID' or key == '漏洞类型':
                print(key,':\t',value)
            else:
                print(key,':\t',fun.trans(value))
        print('='*50)
'''







'''
url_google = 'http://translate.google.cn'
reg_text = re.compile(r'(?<=TRANSLATED_TEXT=).*?;')
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                r'Chrome/44.0.2403.157 Safari/537.36'

def translateGoogle(text, f='en', t='zh-cn'):
    values = {'hl': 'zh-cn', 'ie': 'utf-8', 'text': text, 'langpair': '%s|%s' % (f, t)}
    value = urllib.parse.urlencode(values)
    req = urllib.request.Request(url_google + '?' + value)
    req.add_header('User-Agent', user_agent)
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    data = reg_text.search(content)
    # result = data.group(0).strip(';').strip('\'')
    print(data)
'''