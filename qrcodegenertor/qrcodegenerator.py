import qrcode
import pyqrcode
import sqlite3
from PIL import Image, ImageFont, ImageDraw
#url = pyqrcode.create('http://uca.edu')
#url.svg('uca-url.svg', scale = 8)
#url.eps('uca-url.eps', scale = 2)
#print(url.terminal(quiet_zone=1))
def Product_num_list():
	try:
		db = sqlite3.connect('../db.sqlite3')
		cursor = db.cursor()
		cursor2 = db.cursor()
#	cursor.execute('SELECT name from sqlite_master where type= "table"')
#	print(cursor.fetchall())
		cursor.execute('SELECT product_num FROM \'StockSystem_product\'')
		cursor2.execute('SELECT name FROM \'StockSystem_product\'')
		return cursor.fetchall(), cursor2.fetchall()
#		for i in cursor.fetchall():
#			print(i[0])
		#print("connect OK")
#		return cursor
		#qrcodegenerator(cursor.fetchone())
	except Exception as e:
		print(e)

	finally:
		cursor.close()
		cursor2.close()

def qrcodegenerator(product_num):
	img = qrcode.make("http://localhost:8000/product/"+product_num[0])
	icon = Image.open("./plant.png")
	img_w, img_h = img.size
	factor = 4
	size_w = int(img_w/factor)
	size_h = int(img_h/factor)

	icon_w, icon_h = icon.size
	if icon_w > size_w:
		icon_w = size_w
	if icon_h > size_h:
		icon_h = size_h
	
	icon = icon.resize((icon_w, icon_h), Image. NEAREST)

	w = int((img_w - icon_w)/2)
	h = int((img_h - icon_h)/2)
	img.paste(icon, (w,h), icon)
	img.show()	

	img.save("test1.png")

def imgtest(url, product_number, name):
	qrc = qrcode.make(url+product_number)
	print(qrc.pixel_size)
	W, H =(qrc.pixel_size, int(qrc.pixel_size*1.2))
	img = Image.new('RGB', (W, H), color = 'white')
	msg = name+"  "+product_number
	d = ImageDraw.Draw(img)
	w, h = d.textsize(msg)
	imgf = ImageFont.truetype(font = 'TaipeiSansTCBeta-Bold.ttf', size = 16, encoding = 'utf-8')
	img.paste(qrc, (0,0))
	d.text((int((W-w)/2), int(H*0.85)), msg, align=('center'), fill=(0, 0, 0), font = imgf)

	img.show()


def main():
	num_list, product_name = Product_num_list()
	for number, name in zip(num_list, product_name):
		imgtest("http://nater-pos.natertek.com/sold/", number[0], name[0])
#	print(num_list.fetchall())
#	qrcodegenerator(num_list.fetchone())

if __name__ == '__main__':
	main()
