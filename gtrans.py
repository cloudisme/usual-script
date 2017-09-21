#coding=utf-8
#!/usr/bin/python

import execjs
import urllib2
  
class Gtrans():  

    def __init__(self):
        self.url = "http://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s"
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

    # 翻译
    def translate(self, text):
        # 长度限制（因为是get请求）   
        if len(text) > 4000:
            print u"翻译的长度超过限制"
            return ""
        try:
            # 构造url
            tk   = self.get_tk(text)
            text = text.encode('utf8')
            text = urllib2.quote(text)
            url  = self.url % (tk, text)
            # 请求
            result = self.request(url)
        except:
            result = ""
        # 处理结果并返回
        end = result.find("\",")
        if end > 4:
            return result[4:end]
        else:
            return ""

    # 请求
    def request(self, url):
        header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control':'max-age=0',
            'Host':'translate.google.cn',
            'Upgrade-Insecure-Requests':1,
            'Referer':None,
            'Content-Type':'application/json; charset=UTF-8',
            'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        req = urllib2.Request(url, None, header)
        req = urllib2.urlopen(req)
        ret = req.read()
        return ret

    # 获取tk值
    def get_tk(self,text):
        return self.ctx.call("TL",text)

# 运行
if __name__ == '__main__':
    gt = Gtrans()
    print gt.translate("hello world")