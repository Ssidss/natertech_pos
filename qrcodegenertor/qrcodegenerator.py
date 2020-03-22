import qrcode
import pyqrcode
import sqlite3
from PIL import Image
#url = pyqrcode.create('http://uca.edu')
#url.svg('uca-url.svg', scale = 8)
#url.eps('uca-url.eps', scale = 2)
#print(url.terminal(quiet_zone=1))
def Product_num_list():
	try:
		db = sqlite3.connect('../db.sqlite3')
		cursor = db.cursor()
#	cursor.execute('SELECT name from sqlite_master where type= "table"')
#	print(cursor.fetchall())
		cursor.execute('SELECT product_num FROM \'StockSystem_product\'')
#		for i in cursor.fetchall():
#			print(i[0])
		print("connect OK")
#		return cursor
		qrcodegenerator(cursor.fetchone())
	except Exception as e:
		print(e)

	finally:
		cursor.close()

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

def main():
	num_list = Product_num_list()
#	print(num_list.fetchall())
#	qrcodegenerator(num_list.fetchone())

if __name__ == '__main__':
	main()
