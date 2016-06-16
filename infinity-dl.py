#!/usr/bin/env python
from bs4 import BeautifulSoup
import sys, shutil, requests, time, os, random

argv = sys.argv
chan_list = ["8ch.net", "hispachan.org", "4chan.org", "7chan.org"]
server_err = [404, 401, 500, 502, 403, 400]
def _err_():
	sys.stderr.write("Usage: " + argv[0] + " [URL] [DIR]\n")
def send_request():
	sys.stdout.write("\n")
	sys.stdout.flush()
	sys.stdout.write("\033[32m\033[5mSending request...\n")
	sys.stdout.flush()
	sys.stdout.write("\033[0m\033[0m \n")
	sys.stdout.flush()
def server_status_err():
    global url
    url = requests.get(argv[1], verify=True)
    for errors in server_err:
        if url.status_code == errors:
            print(str(url.status_code)  + " Error\n")
            sys.exit()
def _7ch_scraper():
	server_status_err()
	parse_html = BeautifulSoup(url.text, "lxml")
	for p_tags in parse_html.find_all("p", {"class": "file_size"}):
		for a_tags in p_tags.find_all("a"):
			url = a_tags.get("href")
			for the_url in a_tags:
				file_names = []
				file_names.append(the_url.split("/")[-1])
				for names in file_names:
					filenames = names
					get_files = requests.get(url, stream=True, verify=True)
					print("Downloading " + filenames)
					with open(filenames, "wb")as outfile:
						shutil.copyfileobj(get_files.raw, outfile)
						shutil.move(filenames, argv[2])
					del get_files
def _8ch_scraper():
		server_status_err()
		parse_html = BeautifulSoup(url.text, "lxml")
		for tags in parse_html.find_all("div", {"class" : "file"}):
			for span in tags.find_all("p", {"class" : "fileinfo"}):
				for post_file_name  in span.find_all("span", {"class": "postfilename"}):
					filenames = post_file_name.get_text()
				for a_tags in span.find_all("a"):
					media_list = a_tags.get("href")
					change_filename = random.randint(1,1000)
					change_filename = str(change_filename)
					filenames = change_filename + filenames
					r = requests.get(media_list, stream=True, verify=True)
					print("Downloading " + filenames)
					with open(filenames, "wb") as out_file:
						shutil.copyfileobj(r.raw, out_file)
						shutil.move(filenames, argv[2])
					del r
def _4chan_scraper():
	server_status_err()
	parse_html = BeautifulSoup(url.text, "lxml")
	for tags in parse_html.find_all("div", {"class": "fileText"}):
		for a_tags in tags.find_all("a"):
			usplit_link = a_tags.get("href")
			media_list_url = "https://" + usplit_link.split("//")[-1]
			filenames = a_tags.get_text()
			change_filename = random.randint(1,1000)
			change_filename = str(change_filename)
			filenames = change_filename + filenames
			get_files = requests.get(media_list_url, stream= True, verify=True)
			print("Downloading "+ filenames)
			with open(filenames, "wb")as outfile:
				shutil.copyfileobj(get_files.raw, outfile)
				shutil.move(filenames, argv[2])
			del get_files
def hispanchan():
		server_status_err()
		parse_html = BeautifulSoup(url.text, "lxml")
		for span in parse_html.find_all('span',{'class' : 'filenamereply'}):
			for a_tags in span.find_all('a'):
				filenames = a_tags.get('href').split('/')[-1]
				media_list_url = a_tags.get('href')
				change_filename = random.randint(1,1000)
				change_filename = str(change_filename)
				filenames = change_filename + filenames
				get_files = requests.get(media_list_url, stream=True, verify=True)
				print("Downloading "+ filenames)
				with open(filenames, 'wb')as outfile:
					shutil.move(filenames, argv[2])
					shutil.copyfileobj(get_files.raw, outfile)
def main():
	if (len(argv) > 3) and (os.path.isdir(argv[2]) == False):
		_err_()
		sys.exit()
	elif (len(argv) < 3) or (os.path.isdir(argv[2]) == False):
		_err_()
		sys.exit()
	for chan in chan_list:
		if chan in argv[1]:
			send_request()
			_4chan_scraper()
			_8ch_scraper()
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt or IndexError:
		print("  \n")
		print("\033[31mDownload interrupted\n")
		sys.exit()
