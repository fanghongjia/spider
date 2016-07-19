import pytesseract
from PIL import Image
import urllib  
# url = r"http://www.kali.org.cn/plugin.php?id=cloudcaptcha:get&rand=UvpS0Kdysk"  
# path = r"idcode.jpg"  
# data = urllib.urlretrieve(url,path) 
image = Image.open('2.jpg')
vcode = pytesseract.image_to_string(image)
print vcode


function checksec(type, idhash, showmsg, recall) {
	$F('_checksec', arguments);
}

