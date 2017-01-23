import sys
import time
from urlToObject import url_to_text
from textSearcher import html_wrapper


def main(args):
    """ test urls
    url = 'https://www.nytimes.com/2017/01/19/us/trump-cabinet-picks-inauguration.html'

    todo
    #http://time.com/4642876/donald-trump-presidency-first-days-inauguration/?xid=homepage
    #http://time.com/4642838/samsung-galaxy-note-seven-smartphones-overheating-explanation/

    reuters
    AP
    The Telegraph
    The Guardian
    Thinkprogress
    salon
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

    consider:
    adding author quals detector

    blacklist:
    breitbart
    thinkprogress?
    """

    urls = ['']
    """['http://www.foxnews.com/politics/2017/01/23/trumps-cabinet-picks-face-questions-from-both-parties-mcconnell-confident.html',
            'https://www.nytimes.com/2017/01/19/us/trump-cabinet-picks-inauguration.html',
            'http://www.politico.com/story/2017/01/alternative-facts-kellyanne-conway-233998']"""

    for url in urls:

        article_html_text = url_to_text(url)

        title_cached, date_cached, author_cached, body_cached = False, False, False, False
        t_cache, d_cache, a_cache, b_cache = [], [], [], []
        tags, nicknames = {}, {}
        reverse_nicknames = {}

        if ('nytimes.com' in url):
            tags = {'title': [], 'span': ['byline-author'], 'p': ['story-body-text story-content']}
            nicknames = {'title': 'title', 'span': 'authors', 'p': 'body'}

            """ nyt date handler- just have function that splits url when this is fed in
            and takes in series of numbers indicating tokens"""

            publish_date = url[url.find('nytimes.com') + len('nytimes.com'):]
            date_tokens = publish_date.split('/')
            year = date_tokens[1]
            month = date_tokens[2]
            day = date_tokens[3]
            d_cache.append((month + '-' + day + '-' + year))
            date_cached = True
        if ('politico.com' in url):
            tags = {'title': [], 'dt': ['credits-author'], 'time': [], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'time': 'date', 'dt': 'authors', 'p': 'body'}
        if ('foxnews.com' in url):
            tags = {'title': [], 'div': ['article-text']}
            nicknames = {'title': 'title', 'div': 'body'}

            a_cache = 'Fox News'
            author_cached = True

            publish_date = url[url.find('foxnews.com') + len('foxnews.com'):]
            date_tokens = publish_date.split('/')
            year = date_tokens[2]
            month = date_tokens[3]
            day = date_tokens[4]
            d_cache.append((month + '-' + day + '-' + year))
            date_cached = True
        if ('time.com' in url):
            tags = {'h1': ['article-title'], 'ul': ['article-authors']}
            nicknames = {'title': 'title', 'ul': 'authors'}

        for key in nicknames:
            reverse_nicknames[nicknames[key]] = key

        output_text = html_wrapper(article_html_text, tags, nicknames)

        if (title_cached is False and output_text['title'] != []):
            t_cache = output_text['title']
            title_key = reverse_nicknames['title']
            tags.pop(title_key)
            nicknames.pop(title_key)
            title_cached = True
        if (date_cached is False and output_text['date'] != []):
            d_cache = output_text['date'][0]
            date_key = reverse_nicknames['date']
            tags.pop(date_key)
            nicknames.pop(date_key)
            date_cached = True
        if (author_cached is False and output_text['authors'] != []):
            a_cache = output_text['authors']
            author_key = reverse_nicknames['authors']
            tags.pop(author_key)
            nicknames.pop(author_key)
            author_cached = True
        if (body_cached is False and output_text['body'] != []):
            b_cache = output_text['body']
            body_key = reverse_nicknames['body']
            tags.pop(body_key)
            nicknames.pop(body_key)
            body_cached = True

        """ Ensure it doesn't do that stupid bug where randomly shit isn't returned in request text. """
        while (title_cached is False or author_cached is False or body_cached is False):
            output_text = html_wrapper(article_html_text, tags, nicknames)
            if (title_cached is False and output_text['title'] != []):
                t_cache = output_text['title']
                title_key = reverse_nicknames['title']
                tags.pop(title_key)
                nicknames.pop(title_key)
                title_cached = True
            if (date_cached is False and output_text['date'] != []):
                d_cache = output_text['date'][0]
                date_key = reverse_nicknames['date']
                tags.pop(date_key)
                nicknames.pop(date_key)
                date_cached = True
            if (author_cached is False and output_text['authors'] != []):
                a_cache = output_text['authors']
                author_key = reverse_nicknames['authors']
                tags.pop(author_key)
                nicknames.pop(author_key)
                author_cached = True
            if (body_cached is False and output_text['body'] != []):
                b_cache = output_text['body']
                body_key = reverse_nicknames['body']
                tags.pop(body_key)
                nicknames.pop(body_key)
                body_cached = True

        """ ugh, need to organize handlers- here we handle any weird cases
        of titles or authors containing stupid text on the end """
        if ('nytimes.com' in url):
            t_cache[0] = t_cache[0].replace(' - The New York Times', '')
        if ('politico.com' in url):
            d_cache = d_cache[:8]
            print(d_cache)
            d_cache = d_cache.replace("/", "-")
            """ sometimes this above line an error... why..... makes it a list. """
            b_cache = [item for item in b_cache if 'AP Photo' not in item]
        if ('time.com' in url):
            if ('AM' in d_cache[0] or 'PM' in d_cache[0]):
                """ If TIME gives date published in their html as a specific time, it was published today. """
                d_cache = time.strftime("%m-%d-%Y")
        if ('foxnews.com' in url):
            t_cache[0] = t_cache[0].replace(' | Fox News', '')
            cite = a_cache + ', ' + d_cache + ', "' + t_cache[0] + '", ' + url
        else:
            """ Create author names. """
            a_cache = [remove_brackets(item) for item in a_cache]
            authors_last = ''
            authors_first = ''
            for author in a_cache:
                author_tokens = author.split()
                if (authors_last != ''):
                    authors_last += ' and '
                    authors_first += ' and '
                authors_first += author_tokens[0].lower().capitalize()
                authors_last += author_tokens[-1].lower().capitalize()

            """ Create cite. """
            cite = authors_last + ', ' + d_cache + ', ' + authors_first + ', "' + t_cache[0] + '", ' + url

        """ Create body. """
        body = b_cache
        text = ''
        for para in body:
            para = remove_brackets(para)
            text += (para + '\n')

        """ Card is cite + body. """
        card = cite + '\n\n' + text + '\n\n'

        """ Get rid of stupid html equivalent expressions (e.g. Fox uses the
        html code for quotation marks instead of just using quotes in the html). """
        card = remove_common_artifacts(card)

        f = open('card output', 'a')

        """ Write card to output file."""
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
