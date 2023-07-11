import requests # handle requests and image download (pip install requests)
import os # handle folder creation 
import urllib # handle href parser, image extension and get main url (pip install urllib3)
import shutil # handle folder deletion (pip install pytest-shutil)
from bs4 import BeautifulSoup as bs # handle html (pip install beautifulsoup4)
import time # handle sleep 
import cv2 # handle image concatenation (pip install opencv-python)
from PIL import Image # handle image verification (pip install Pillow)
from PIL import ImageFile # handle truncated image read (pip install Pillow)
import numpy as np # handle image concatenation (pip install numpy)
from termcolor import colored # handle colored terminal (pip install termcolor)
from colorama import init # handle colored terminal (pip install colorama)
import tkinter as tk # handle GUI (pip install tk)
import tkinter.ttk as ttk # handle GUI (pip install tk)
import tkinter.messagebox as msgb # handle messagebox (pip install tk)
from tqdm.auto import tqdm # handle progress bar (pip install tqdm)

init()

ImageFile.LOAD_TRUNCATED_IMAGES = True

# tôi lười chú thích được chưa....

def make_window():
	def close():
		flag1 = flag2 = 0

		def check(url):
			with requests.Session() as s:
				try:
					site = s.get(url, stream = True, timeout = 30)
				except:
					return 0

			site.close()

			return 1

		if (check(manga_url_tk.get().strip()) == 0):
			flag1 = 1
		if (download_all_tk.get() == 0 and concatenated_original_image_value_tk.get() == 0 and concatenated_stretched_image_value_tk.get() == 0 and stretched_image_pdf_value_tk.get() == 0 and original_image_pdf_value_tk.get() == 0):
			flag2 = 1

		if (flag1 == 1 or flag2 == 1):
			error = ''

			if (flag1 == 1):
				error += 'Vui lòng nhập một link hợp lệ !\n'
			if (flag2 == 1):
				error += 'Vui lòng chọn ít nhất một phương án download !\n'

			msgb.showerror(title = 'Lỗi', message = error)

			return

		window.destroy()

	class ToolTip():
		def __init__(self, widget, text):
			self.widget = widget
			self.tipwindow = None
			self.text = text
			self.widget.bind('<Enter>', self.showtip)
			self.widget.bind('<Leave>', self.hidetip)

		def showtip(self, text):
			if self.tipwindow != None or not self.text:
				return
			x, y, cx, cy = self.widget.bbox('insert')
			x = x + self.widget.winfo_rootx() + 25
			y = y + cy + self.widget.winfo_rooty() + 20

			self.tipwindow = tw = tk.Toplevel(self.widget)

			tw.wm_overrideredirect(1)
			tw.wm_geometry('+%d+%d' % (x, y))
			label = tk.Label(tw, text = self.text, justify = tk.LEFT, bg = '#474747', fg = '#ffffff', relief = tk.SOLID, borderwidth = 1, font = ('arial', 10, 'bold'))
			label.pack(ipadx = 5, ipady = 5)

		def hidetip(self, text):
			tw = self.tipwindow
			self.tipwindow = None
			if tw:
				tw.destroy()

	window = tk.Tk()
	window.title('Manga downloader')
	window.geometry('900x600')
	window.resizable(False, False)
	window.configure(bg = '#474747')

	label = tk.Label(window, text = 'Nhập link manga', font = ('tahoma', 15, 'bold'))
	label.configure(bg = '#474747', fg = '#ffffff')
	label.pack()

	manga_url_tk = tk.StringVar()
	manga_url_tb = ttk.Entry(window, width = 120, background = 'light cyan', font = ('tahoma', 10, 'normal'), textvariable = manga_url_tk)
	manga_url_tb.pack(ipadx = 5, ipady = 5, pady = 20)

	download_all_tk = tk.IntVar()
	download_all_cb = ttk.Checkbutton(window, text = 'Download all ?', variable = download_all_tk, onvalue = 1, offvalue = 0)
	download_all_cb.pack(pady = 15)

	concatenated_original_image_value_tk = tk.IntVar()
	concatenated_original_image_value_cb = ttk.Checkbutton(window, text = 'Long strip images (Original size) ?', variable = concatenated_original_image_value_tk, onvalue = 1, offvalue = 0)
	concatenated_original_image_value_cb.pack(pady = 15)

	concatenated_stretched_image_value_tk = tk.IntVar()
	concatenated_stretched_image_value_cb = ttk.Checkbutton(window, text = 'Long strip images (Stretched) ?', variable = concatenated_stretched_image_value_tk, onvalue = 1, offvalue = 0)
	concatenated_stretched_image_value_cb.pack(pady = 15)

	original_image_pdf_value_tk = tk.IntVar()
	original_image_pdf_value_cb = ttk.Checkbutton(window, text = 'PDF files (Original size) ?', variable = original_image_pdf_value_tk, onvalue = 1, offvalue = 0)
	original_image_pdf_value_cb.pack(pady = 15)

	stretched_image_pdf_value_tk = tk.IntVar()
	stretched_image_pdf_value_cb = ttk.Checkbutton(window, text = 'PDF files (Stretched) ?', variable = stretched_image_pdf_value_tk, onvalue = 1, offvalue = 0)
	stretched_image_pdf_value_cb.pack(pady = 15)

	end_value_tk = tk.IntVar()
	end_value_cb = ttk.Checkbutton(window, text = 'End ?', variable = end_value_tk, onvalue = 1, offvalue = 0)
	end_value_cb.pack(pady = 15)

	download_button = ttk.Button(window, text = 'Download', command = close)
	download_button.pack(pady = 15)

	description1 = 'Link của manga'
	description2 = 'Nhấn để bắt đầu download'
	description3 = 'Download toàn bộ manga và mỗi chapter để trong 1 thư mục riêng'
	description4 = 'Tạo một ảnh dài để đọc (kích cỡ gốc) (từng chapter)'
	description5 = 'Tạo một ảnh dài để đọc (đã phóng to) (từng chapter)'
	description6 = 'Tạo một file PDF để đọc (kích cỡ gốc) (từng chapter)'
	description7 = 'Tạo một file PDF để đọc (đã phóng to) (từng chapter)'
	description8 = 'Manga đã end hay chưa'

	ToolTip(manga_url_tb, text = description1)
	ToolTip(download_button, text = description2)
	ToolTip(download_all_cb, text = description3)
	ToolTip(concatenated_original_image_value_cb, text = description4)
	ToolTip(concatenated_stretched_image_value_cb, text = description5)
	ToolTip(original_image_pdf_value_cb, text = description6)
	ToolTip(stretched_image_pdf_value_cb, text = description7)
	ToolTip(end_value_cb, text = description8)

	window.mainloop()

	manga_url = manga_url_tk.get().strip()
	download_all = download_all_tk.get()
	concatenated_original_image_value = concatenated_original_image_value_tk.get()
	concatenated_stretched_image_value = concatenated_stretched_image_value_tk.get()
	stretched_image_pdf_value = stretched_image_pdf_value_tk.get()
	original_image_pdf_value = original_image_pdf_value_tk.get()
	end_value = end_value_tk.get()

	return [manga_url, download_all, concatenated_original_image_value, concatenated_stretched_image_value, stretched_image_pdf_value, original_image_pdf_value, end_value]

def name_cleanup(x):
	x = ' '.join(x.split())

	x = str(x).strip()
	x = str(x).strip('.')

	spe_chars = '\t\n\b\v\f\a'
	bad_chars = r'\/:*?"<>|'
	translator = {}
	for spe_char in spe_chars:
		translator[spe_char] = ' '
	for bad_char in bad_chars:
		if (bad_char == ':'): translator[bad_char] = '.'
		else: translator[bad_char] = ''

	return x.translate(str.maketrans(translator))

def create_name(name, ext):
	return (name_cleanup(name) + ext.strip())

def create_path(path, name, ext): # tạo đường dẫn hợp lệ
	name = name_cleanup(name)

	path = os.path.join(path, name.strip() + ext.strip())

	path = str(path).strip('.')

	return path

def make_folder(path, name): # tạo thư mục 
	path = create_path(path, name, '')

	try:
		os.makedirs(path)
	except OSError:
		shutil.rmtree(path)
		os.makedirs(path)

	return path

def get_dict_values(data_structure): # lấy giá trị của dict
	[*values] = data_structure.values()

	return values

def get_list_values(data_structure, tmp): # lấy giá trị của list
	for item in data_structure:
		if (type(item) == list):
			tmp = get_list_values(item, tmp)
		elif (type(item) == dict):
			dict_values = get_dict_values(item)
			tmp = get_list_values(dict_values, tmp)
		else:
			tmp.append(item)

	return tmp

def get_object_values(data_structure, res): # lấy giá trị của 1 object bất kì
	if (type(data_structure) == dict):
		values = get_dict_values(data_structure)
		
		return get_object_values(values, res)
	if (type(data_structure) == list):
		return get_list_values(data_structure, res)

	res.append(data_structure)

	return res

def write_file(path, file_name, ext, type, spacing, things_to_write): # tạo một file ở đường dẫn cho trước
	type_to_edit = 'w'
	if (type == 0):
		type_to_edit = 'w'
	if (type == 1):
		type_to_edit = 'a'
	if (type == 2):
		type_to_edit = 'wb'

	path = create_path(path, file_name, ext)

	new_things = get_object_values(things_to_write, res = [])

	if (type == 2):
		f = open(path, type_to_edit)

		for x in new_things:
			f.write(x)

		f.close()

		return
	else: f = open(path, type_to_edit, encoding = 'utf-8')

	for x in new_things:
		f.write(str(x))
		for i in range(spacing):
			f.write('\n')

	f.close()

def get_image(chapter_path, image_url, image_cnt, headers):
	image_ext = os.path.splitext(urllib.parse.urlparse(image_url).path)[1]

	if (image_ext == ''): image_ext = '.png'
	
	image_path = create_path(chapter_path, f'Image ({image_cnt})', image_ext)

	attempt = 0
	while (1):
		try:
			image = requests.get(image_url, headers = headers, stream = True, timeout = 30).content

			if (image == 'URL signature expired'.encode('utf-8')):
				return 0

			write_file(chapter_path, f'Image ({image_cnt})', image_ext, 2, 0, image)

			image_file = Image.open(image_path)

			image_file.verify()
		except Exception as err:
			attempt += 1
			seconds = 5
			print(colored(f'Error: {err}', 'red'))
			print(colored(f'Error occurred at: {image_url}', 'red'))
			print(colored(f'Try again in {seconds}s, attempt: {attempt}', 'red'))
			time.sleep(seconds)
		else:
			break

	return image_path

def get_image_list(image_path_list):
	if (len(image_path_list) > 0):
		image_list = []
		pdf_image_list = []

		for image_path in image_path_list:
			while (1):
				try:
					image_pdf = Image.open(image_path).convert('RGB')
					image_cv2 = np.array(Image.open(image_path).convert('RGB'))[:, :, ::-1].copy()
				except:
					continue
				else:
					break

			if (len(image_cv2.shape) < 3):
				image_cv2 = cv2.cvtColor(image_cv2, cv2.COLOR_GRAY2RGBA)
			if (len(image_cv2.shape) < 4):
				image_cv2 = cv2.cvtColor(image_cv2, cv2.COLOR_RGB2RGBA)

			image_list.append(image_cv2)
			pdf_image_list.append(image_pdf)

		return [image_list, pdf_image_list]

def connect_image(image_list, interpolation = cv2.INTER_CUBIC):
	max_w = max(image.shape[1] for image in image_list)

	resized_image_list = [cv2.resize(image, [max_w, int(image.shape[0] * max_w / image.shape[1])], interpolation = interpolation) for image in image_list]

	return cv2.vconcat(resized_image_list)

def get_concatenated_image(path, name, stretched, image_list):
	if (len(image_list) > 0):
		image_ext = '.png'

		all_image_path = create_path(path, name, image_ext)

		if (stretched == 1):
			final_image = connect_image(image_list)
		else:
			max_w = 0
			total_h = 0

			for image in image_list:
				max_w = max(max_w, image.shape[1])
				total_h += image.shape[0]

			final_image = np.zeros((total_h, max_w, 4), dtype = np.uint8)

			cur_y = 0

			for image in image_list:
				image = np.hstack((image, np.zeros((image.shape[0], max_w - image.shape[1], 4))))
				final_image[cur_y : cur_y + image.shape[0], :, :] = image
				cur_y += image.shape[0]

		is_success, image_buf_arr = cv2.imencode(image_ext, final_image)

		image_buf_arr.tofile(all_image_path)

		return all_image_path

def get_pdf(path, name, stretched, image_list):
	if (len(image_list) > 0):
		pdf_path = create_path(path, name, '.pdf')

		if (stretched == 1):
			max_w = 0

			for image in image_list:
				w, h = image.size

				max_w = max(max_w, w)

			resized_image_list = []

			for image in image_list:
				w, h = image.size

				aspect_ratio = w / h

				new_w = max_w
				new_h = int(new_w / aspect_ratio)

				image = image.resize((new_w, new_h), Image.ANTIALIAS)

				resized_image_list.append(image)

			image1 = resized_image_list[0]
			del(resized_image_list[0])

			image1.save(pdf_path, 'pdf', resolution = 100.0, save_all = True, append_images = resized_image_list)
		else:
			_image_list = image_list[:]
			image1 = _image_list[0]
			del(_image_list[0])

			image1.save(pdf_path, 'pdf', resolution = 100.0, save_all = True, append_images = _image_list)

		return pdf_path

def get_chapter(chapter_link, chapter_name, chapter_path, concatenated_original_image_value, concatenated_stretched_image_value, original_image_pdf_value, stretched_image_pdf_value, headers): # download một chapter truyện
	with requests.Session() as s:
		attempt = 0
		while (1):
			try:
				chapter_site = s.get(chapter_link, headers = headers, stream = True, timeout = 30)
				html_chapter_contents = bs(chapter_site.content, 'html.parser')

				html_image_url_list = html_chapter_contents.findAll('div', {'class': 'page-chapter'})
			except Exception as err:
				attempt += 1
				seconds = 5
				print(colored(f'Error: {err}', 'red'))
				print(colored(f'Error occurred at: {image_url}', 'red'))
				print(colored(f'Try again in {seconds}s, attempt: {attempt}', 'red'))
				time.sleep(seconds)
			else:
				break

	image_cnt = 0
	corrupted_image_cnt = 0

	chapter_image_path_list = []

	print(f'Downloading chapter: {chapter_name}')

	# for html_image_url in tqdm(html_image_url_list):
	for html_image_url in html_image_url_list:
		image_url = html_image_url.find('img').get('src')
		parsed_image_url = urllib.parse.urlparse(image_url)

		image_cnt += 1

		if (len(parsed_image_url.scheme) == 0):
			image_url = urllib.parse.urljoin('http://', image_url)

		res = get_image(chapter_path, image_url, image_cnt, headers)

		if (res == 0):
			corrupted_image_cnt += 1
		else:
			chapter_image_path_list.append(res)

		print(f'Downloaded {image_cnt} / {len(html_image_url_list)} image(s)', end = '\r')

	concatenated_image_name = pdf_name = f'{chapter_name}'

	image_list, pdf_image_list = get_image_list(chapter_image_path_list)

	concatenated_image_original_path = ''
	concatenated_image_stretched_path = ''
	original_image_pdf_path = ''
	stretched_original_image_pdf_path = ''

	if (concatenated_original_image_value == 1): concatenated_image_original_path = get_concatenated_image(chapter_path, f'{concatenated_image_name} (Original)', 0, image_list)
	if (concatenated_stretched_image_value == 1): concatenated_image_stretched_path = get_concatenated_image(chapter_path, f'{concatenated_image_name} (Stretched)', 1, image_list)
	if (original_image_pdf_value == 1): original_image_pdf_path = get_pdf(chapter_path, f'{pdf_name} (Original)', 0, pdf_image_list)
	if (stretched_image_pdf_value == 1): stretched_original_image_pdf_path = get_pdf(chapter_path, f'{pdf_name} (Stretched)', 1, pdf_image_list)

	print(colored(f'Downloaded chapter: {chapter_name}.\nImage count: {image_cnt - corrupted_image_cnt}, corrupted image count: {corrupted_image_cnt}\n', 'magenta'))

	return [concatenated_image_original_path, concatenated_image_stretched_path, original_image_pdf_path, stretched_original_image_pdf_path]

	chapter_site.close()

def get_manga(window_element_list):
	manga_url = window_element_list[0]
	download_all = window_element_list[1]
	concatenated_original_image_value = window_element_list[2]
	concatenated_stretched_image_value = window_element_list[3]
	stretched_image_pdf_value = window_element_list[4]
	original_image_pdf_value = window_element_list[5]
	end_value = window_element_list[6]

	parsed_url = urllib.parse.urlsplit(manga_url)
	main_url = f'{parsed_url[0]}://{parsed_url[1]}'

	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
	'referer': main_url,
}
	with requests.Session() as s:
		attempt = 0
		while (1):
			try:
				site = s.get(manga_url, headers = headers, stream = True, timeout = 30)
				site_html_content = bs(site.content, 'html.parser')

				manga_name = site_html_content.find('meta', {'property': 'og:title'}).get('content')

				if (type(manga_name) == None):
					raise Exception

				manga_name = name_cleanup(manga_name)
			except Exception as err:
				attempt += 1
				seconds = 5
				print(colored(f'Error: {err}', 'red'))
				print(colored(f'Error occurred at: {manga_url}', 'red'))
				print(colored(f'Try again in {seconds}s, attempt: {attempt}', 'red'))
				time.sleep(seconds)
			else:
				break
	
	if (end_value == 1): manga_name += ' (End)'
	else: manga_name += ' (Processing)'

	print(f'Manga: {manga_name}', end = '\n\n')

	html_chapter_link_list = site_html_content.findAll('div', {'class': 'col-xs-5 chapter'})
	html_chapter_link_list.reverse()

	print(colored(f'Chapter count: {len(html_chapter_link_list)}', 'green'))

	chapter_cnt = 0
	chapter_element_list = []
	for html_chapter_link in html_chapter_link_list:
		chapter_cnt += 1

		chapter_elements = []

		chapter_elements.append(html_chapter_link.find('a').get('href'))
		chapter_elements.append(name_cleanup(f'({chapter_cnt}) {name_cleanup(html_chapter_link.text)}'))

		chapter_element_list.append(chapter_elements)

	manga_path = make_folder(os.getcwd(), manga_name)
	if (concatenated_original_image_value == 1): all_chapter_concatenated_image_original_path = make_folder(manga_path, 'All chapter concatenated images (Original)')
	if (concatenated_stretched_image_value == 1): all_chapter_concatenated_image_stretched_path = make_folder(manga_path, 'All chapter concatenated images (Stretched)')
	if (original_image_pdf_value == 1): all_chapter_original_pdf_path = make_folder(manga_path, 'All chapter PDF (Original)')
	if (stretched_image_pdf_value == 1): all_chapter_stretched_pdf_path = make_folder(manga_path, 'All chapter PDF (Stretched)')

	for chapter_elements in chapter_element_list:
		chapter_link = chapter_elements[0]
		chapter_name = chapter_elements[1]

		chapter_path = make_folder(manga_path, chapter_name)

		concatenated_image_path = get_chapter(chapter_link, chapter_name, chapter_path, concatenated_original_image_value, concatenated_stretched_image_value, original_image_pdf_value, stretched_image_pdf_value, headers)

		if (concatenated_original_image_value == 1): shutil.copy(concatenated_image_path[0], all_chapter_concatenated_image_original_path)
		if (concatenated_stretched_image_value == 1): shutil.copy(concatenated_image_path[1], all_chapter_concatenated_image_stretched_path)
		if (original_image_pdf_value == 1): shutil.copy(concatenated_image_path[2], all_chapter_original_pdf_path)
		if (stretched_image_pdf_value == 1): shutil.copy(concatenated_image_path[3], all_chapter_stretched_pdf_path)

		if (download_all == 0):
			shutil.rmtree(chapter_path)

	site.close()

get_manga(make_window())

print('\nDone !')