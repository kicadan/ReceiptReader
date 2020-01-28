import json
import cv2
import pytesseract
import re
import preprocessing

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'


date_Regex = re.compile("(\d{2,4}(\/|\.|\-|\—)\d{2}(\/|\.|\-|\—)\d{2,4})")
product_Regex = re.compile("(.*(x\d+,\d{0,2}).*)")

products = {
	"Products" : []
}

f= open("paragony.txt", "r")
if f.mode == "r":
	receiptNames = f.read()

receiptNames = receiptNames.split("\n")
for receiptName in receiptNames:
	products = {
		"Products": []
	}
	img = cv2.imread(receiptName)
	text = pytesseract.image_to_string(img, config=tessdata_dir_config, lang="pol")
	texts = text.split('\n')
	for x in texts:
		if product_Regex.match(x):
			mid = re.findall("([\d ]+x[ ]*\d+,\d{0,2})", x)[0]
			posFirst = re.search(mid, x).start()
			posLast = re.search(mid, x).end()
			products["Products"].append({
				"Name": x[0:posFirst],
				"Price": re.findall("(\d+,\d{0,2})", x[posLast:len(x)])[0]
				})
		if date_Regex.match(x):
			products["Date"] = re.findall(date_Regex, x)[0][0]
	print(products)
	outputFileName = receiptName.split(".", 1)[0]
	with open("paragony/" + outputFileName + ".json", 'w', encoding='utf-8') as outfile:
		json.dump(products, outfile, ensure_ascii=False, indent=4)
