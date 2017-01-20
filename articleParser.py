import sys
import time
from urlToObject import url_to_text
from textSearcher import html_wrapper

def main(args):

	""" test urls
	url = 'https://www.nytimes.com/2017/01/19/us/trump-cabinet-picks-inauguration.html'
	"""
	

	"""
	todo
	reuters
	AP
	The Telegraph
	The Guardian
	Thinkprogress
	salon
	fox
	nbc
	abc
	cbs
	xinhua
	PR newswire
	RT
	bloomberg
	la times
	usa today
	TIME
	Yahoo News
	NPR
	Daily Beast
	Daily KOS
	National Review
	Heritage Foundation
	CATO
	WSJ
	CNBC
	The Hill
	Seeking alpha
	the independent


	blacklist:
	breitbart
	thinkprogress?
	"""

	url = 'https://www.nytimes.com/2017/01/19/us/trump-cabinet-picks-inauguration.html'
	article_html_text = url_to_text(url)
	
	title_cached, author_cached, body_cached = False, False, False
	t_cache, a_cache, b_cache = [], [], []
	tags, nicknames = {}, {}
	reverse_nicknames = {}

	if ('nytimes.com' in url):
		tags = {'title': [], 'span': ['byline-author'], 'p':['story-body-text story-content']}
		nicknames = {'title': 'title', 'span': 'authors', 'p': 'body'}

		#nyt date handler
		publish_date = url[url.find('nytimes.com') + len('nytimes.com'):]
		date_tokens = publish_date.split('/')
		year = date_tokens[1]
		month = date_tokens[2]
		day = date_tokens[3]
		publish_date = month + '-' + day + '-' + year

	for key in nicknames:
		reverse_nicknames[nicknames[key]] = key
	
	output_text = html_wrapper(article_html_text, tags, nicknames)

	if (output_text['title'] != []):
		t_cache = output_text['title']
		tags.pop(reverse_nicknames['title'])
		nicknames.pop(reverse_nicknames['title'])
		title_cached = True
	if (output_text['authors'] != []):
		a_cache = output_text['authors']
		tags.pop(reverse_nicknames['authors'])
		nicknames.pop(reverse_nicknames['authors'])
		author_cached = True
	if (output_text['body'] != []):
		b_cache = output_text['body']
		tags.pop(reverse_nicknames['body'])
		nicknames.pop(reverse_nicknames['body'])
		body_cached = True

	#Ensure it doesn't do that stupid bug where randomly shit isn't returned in request text
	while (title_cached is False or author_cached is False or body_cached is False):
		output_text = html_wrapper(article_html_text, tags, nicknames)
		if (title_cached is False and output_text['title'] != []):
			t_cache = output_text['title']
			tags.pop(reverse_nicknames['title'])
			nicknames.pop(reverse_nicknames['title'])
			title_cached = True
		if (author_cached is False and output_text['authors'] != []):
			a_cache = output_text['authors']
			tags.pop(reverse_nicknames['authors'])
			nicknames.pop(reverse_nicknames['authors'])
			author_cached = True
		if (body_cached is False and len(output_text['body']) != []):
			b_cache = output_text['body']
			tags.pop(reverse_nicknames['body'])
			nicknames.pop(reverse_nicknames['body'])
			body_cached = True

	#ugh, need to organize handlers
	if ('nytimes.com' in url):
		article_title = t_cache[0].replace(' - The New York Times', '')
	
	#create author names
	authors_last = ''
	authors_first = ''
	for author in a_cache:
		author_tokens = author.split()
		if (authors_last != ''):
			authors_last += ' and '
			authors_first += ' and '
		authors_first += author_tokens[0].lower().capitalize()
		authors_last += author_tokens[-1].lower().capitalize()

	#create cite
	cite = authors_last + ', ' + publish_date + ', ' + authors_first + ', "' + article_title + '", ' + url

	#create body
	body = b_cache
	text = ''
	for para in body:
		para = remove_brackets(para)
		text += (para + '\n')

	#card is cite + body
	card = cite + '\n\n' + text + '\n\n'

	card = remove_common_artifacts(card)

	f = open('card output', 'a')

	#Write card to output file
	f.write(card)

	f.close()

def remove_common_artifacts(text):
    text = text.replace("&nbsp;", "")
    text = text.replace("&quot;", "\"")
    text = text.replace("&#039;", "'")
    text = text.replace("&#39;", "'")
    text = text.replace("&#8217;", "'")
    text = text.replace("&#8220;", "\"")
    text = text.replace("&#8221;", "\"")
    text = text.replace("&amp;", "&")
    text = text.replace("\\", "")
    text = text.replace("<br>ot", " ")
    return text

def remove_brackets(text):
    len_text = len(text)
    in_brackets = False
    final_text = ""
    for i in range(len_text):
        cur_char = text[i]
        if (cur_char == '<'):
            in_brackets = True
        else:
            if (in_brackets is False):
                final_text += cur_char
            if (cur_char == '>'):
                in_brackets = False
    return final_text

if __name__ == '__main__':
    main(sys.argv)