import sys
import time
from urlToObject import url_to_text
from textSearcher import html_wrapper


def main(args):
    """
    potential quals sites
    huff post
    nyt (see op eds)
    dailykos
    heritage
    cato
    nationalreview

    need support for nested tags- doesnt cut off till sure its lined up- so one div within a first div doesnt fuck it up
    NEED TO FIGURE OUT AUTHOR ISSUE FOR DAILY KOS- for now just marking as dailykos as source

    fox suddenly not working?

    Need to deal with The Hill's text bug...
    'https://thinkprogress.org/trump-reinstates-abortion-restriction-f911f16c758e#.mamg65lyd' ==> binary mode shit
    """

    """
    reuters
    PR newswire
    la times
    TIME
    Yahoo News
    Seeking alpha
    abc



    the independent

    blacklist:
    breitbart
    rolling stone
    powerlineblog.com
    WSJ (just give paywall explanation in message)
    """

    urls = ['']
    """['http://www.foxnews.com/politics/2017/01/23/trumps-cabinet-picks-face-questions-from-both-parties-mcconnell-confident.html',
            'https://apnews.com/b8446cbf5b504b1abaf49eb0d646367b/US-sent-$221-million-to-Palestinians-in-Obamas-last-hours',
            'http://www.dailywire.com/news/12703/president-trump-names-january-20-2017-national-frank-camp',
            'http://www.vox.com/technology/2017/1/23/14341506/ajit-pai-fcc-chair',
            'http://www.nationalreview.com/article/444140/trump-economy-prosperity-will-silence-his-opponents',
            'http://www.usatoday.com/story/tech/news/2017/01/23/best-best-us-jobs-tech-tech-tech/96723738/', 
            'http://www.cnbc.com/2017/01/23/in-stagnant-market-traders-watching-these-reports-for-clues.html',
            'http://www.salon.com/2017/01/24/trumps-war-on-medicaid-our-new-president-wants-to-gut-a-critical-program-for-the-poor/',
            'http://www.npr.org/sections/thetwo-way/2017/01/23/511273522/trump-files-documents-to-shift-management-of-businesses-to-his-sons',
            'https://www.cato.org/publications/policy-analysis/curse-or-blessing-how-institutions-determine-success-resource-rich',
            'http://www.marketwatch.com/story/the-dows-biggest-surge-came-under-this-president-2017-01-23?mod=cx_picks&cx_navSource=cx_picks&cx_tag=other&cx_artPos=7#cxrecs_s',
            'http://www.nbcnews.com/politics/white-house/president-trump-resigns-businesses-leaves-sons-cfo-charge-n711156?cid=par-nbc_20170124']
            'https://www.yahoo.com/news/kellyanne-conway-cites-alternative-facts-in-tense-interview-with-chuck-todd-over-false-crowd-size-claims-171242433.html',
            'https://www.bloomberg.com/news/articles/2017-01-23/beware-the-hedge-fund-wipeout-in-treasuries-as-bearish-bets-soar',
            'http://www.huffingtonpost.com/entry/many-white-women-marched-now-what_us_5884d0dae4b0d96b98c1dd27?section=us_politics',
            'http://thehill.com/policy/healthcare/315387-what-we-know-and-dont-know-about-trumps-healthcare-plans',
            'https://www.nytimes.com/2017/01/19/us/trump-cabinet-picks-inauguration.html',
            'http://www.thedailybeast.com/articles/2017/01/23/trump-s-health-czar-tom-price-was-a-pal-to-big-pharma.html',
            'http://www.dailykos.com/stories/2017/1/22/1622039/-Kentucky-passes-bill-telling-unions-how-to-spend-voluntary-dues-and-House-Speaker-can-t-explain-why',
            'http://www.politico.com/story/2017/01/alternative-facts-kellyanne-conway-233998',
            'http://news.xinhuanet.com/english/2017-01/22/c_136004898.htm',
            'http://www.telegraph.co.uk/news/2017/01/23/donald-trump-lines-executive-actions-meetings-ahead-first-press/',
            'http://www.cbsnews.com/news/georgia-south-carolina-mississippi-devastated-strong-deadly-storms-tornadoes/',
            'https://www.theguardian.com/us-news/2017/jan/22/white-house-refuses-release-trump-tax-returns-wikileaks',
            'https://www.rt.com/news/374837-russia-us-joint-airstrikes-syria/',
            'http://www.heritage.org/research/commentary/2016/11/demint-election-oped']"""

    for url in urls:

        article_html_text = url_to_text(url)

        title_cached, date_cached, author_cached, body_cached, extra_cached = False, False, False, False, True
        t_cache, d_cache, a_cache, b_cache, e_cache = [], [], [], [], []
        tags, nicknames = {}, {}
        reverse_nicknames = {}

        if ('nytimes.com' in url):
            tags = {'title': [], 'span': ['byline-author'], 'p': ['story-body-text story-content']}
            nicknames = {'title': 'title', 'span': 'authors', 'p': 'body'}

            """ nyt date handler- TODO: just have function that splits url when this is fed in
            and takes in series of numbers indicating tokens"""

            publish_date = url[url.find('nytimes.com') + len('nytimes.com'):]
            date_tokens = publish_date.split('/')
            year = date_tokens[1]
            month = date_tokens[2]
            day = date_tokens[3]
            d_cache = month + '-' + day + '-' + year
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
            d_cache = month + '-' + day + '-' + year
            date_cached = True
        if ('time.com' in url):
            """ to investigate... """
            tags = {'h1': [], 'ul': ['article-authors'], 'time': ['publish-date'], 'article': []}
            nicknames = {'h1': 'title', 'ul': 'authors', 'time': 'date', 'article': 'body'}
        if ('thehill.com' in url):
            tags = {'title': [], 'span': ['submitted-by'], 'span2': ['submitted-date'], 'p': []}
            nicknames = {'title': 'title', 'span': 'authors', 'span2': 'date', 'p': 'body'}
        if ('huffingtonpost.com' in url):
            tags = {'title': [], 'span': ['author-card__details__name'],
                    'span2': ['timestamp__date--published'], 'p': []}
            nicknames = {'title': 'title', 'span': 'authors', 'span2': 'date', 'p': 'body'}
        if ('bloomberg.com' in url):
            tags = {'title': [], 'div': ['author'], 'time': [], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'div': 'authors', 'time': 'date', 'p': 'body'}
        if ('yahoo.com/news' in url):
            """ to work on """
            tags = {'title': [], 'time': [], 'div': ['author Mb(4px) Mend(4px) D(ib)'], 'p': []}
            nicknames = {'title': 'title', 'time': 'date', 'div': 'authors', 'p': 'body'}
        if ('dailykos.com' in url):
            tags = {'title': [], 'span': ['author-name'], 'p': []}
            nicknames = {'title': 'title', 'span': 'authors', 'p': 'body'}

            publish_date = url[url.find('dailykos.com') + len('dailykos.com'):]
            date_tokens = publish_date.split('/')
            year = date_tokens[2]
            month = date_tokens[3]
            day = date_tokens[4]
            d_cache = month + '-' + day + '-' + year
            date_cached = True
        if ('thedailybeast.com' in url):
            tags = {'title': [], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'p': 'body'}
            author_cached = True

            publish_date = url[url.find('dailykos.com') + len('dailykos.com'):]
            date_tokens = publish_date.split('/')
            year = date_tokens[2]
            month = date_tokens[3]
            day = date_tokens[4]
            d_cache = month + '-' + day + '-' + year
            date_cached = True
        if ('heritage.org' in url):
            tags = {'title': [], 'div': ['date'], 'p': ['byline'], 'p2': ['VANILLA']}
            nicknames = {'title': 'title', 'div': 'date', 'p': 'authors', 'p2': 'body'}
        if ('xinhuanet.com' in url):
            tags = {'title': [], 'p': []}
            nicknames = {'title': 'title', 'p': 'body'}
            author_cached = True

            publish_date = url[url.find('dailykos.com') + len('dailykos.com'):]
            date_tokens = publish_date.split('/')
            month_and_year = date_tokens[2].split('-')
            year = month_and_year[0]
            month = month_and_year[1]
            day = date_tokens[3]
            d_cache = month + '-' + day + '-' + year
            date_cached = True
        if ('theguardian.com' in url):
            tags = {'title': [], 'a': ['tone-colour'], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'a': 'authors', 'p': 'body'}

            publish_date = url[url.find('dailykos.com') + len('dailykos.com'):]
            date_tokens = publish_date.split('/')
            year = date_tokens[2]
            month = date_tokens[3]
            day = date_tokens[4]
            d_cache = month + '-' + day + '-' + year
            date_cached = True
        if ('latimes.com'in url):
            tags = {'title': []}
            nicknames = {'title': 'title'}
        if ('cbsnews.com' in url):
            tags = {'title': [], 'span': ['time'], 'span2': ['source'], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'span': 'date', 'span2': 'authors', 'p': 'body'}
        if ('rt.com' in url):
            tags = {'title': [], 'time': ['date'], 'p': ['VANILLA'], 'div': ['article__summary summary ']}
            nicknames = {'title': 'title', 'time': 'date', 'p': 'body', 'div': 'extra'}
            extra_cached = False
            a_cache = ['RT']
            author_cached = True
        if ('telegraph.co' in url):
            tags = {'title': [], 'span': ['byline__author-name'], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'span': 'authors', 'p': 'body'}

            publish_date = url[url.find('telegraph.co') + len('telegraph.co'):]
            date_tokens = publish_date.split('/')
            year = date_tokens[2]
            month = date_tokens[3]
            day = date_tokens[4]
            d_cache = month + '-' + day + '-' + year
            date_cached = True
        if ('thinkprogress.org' in url):
            tags = {'title': [], 'a': ['link link link--darken link--darker u-baseColor--link'], 'time': [], 'p': []}
            nicknames = {'title': 'title', 'a': 'authors', 'time': 'date', 'p': 'body'}
        if ('nbcnews.com' in url):
            tags = {'title': [], 'span': ['byline_author'], 'time': [], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'span': 'authors', 'time': 'date', 'p': 'body'}
        if ('npr.org' in url):
            tags = {'title': [], 'span': ['date'], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'span': 'date', 'p': 'body'}
            """ need to add function to get author """
            author_cached = True
            a_cache = ['NPR']
        if ('cato.org' in url):
            tags = {'title': [], 'footer': ['byline'], 'span': ['date-display-single'], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'footer': 'authors', 'span': 'date', 'p': 'body'}
        if ('apnews.com' in url):
            tags = {'title': [], 'h4': ['updatedString'], 'h42': ['VANILLA'], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'h4': 'date', 'h42': 'authors', 'p': 'body'}
        if ('abcnews.com' in url):
            tags = {'title': [], 'div': ['author has-bio'], 'span': ['timestamp'], 'p': ['articleBody']}
            nicknames = {'title': 'title', 'span': 'date', 'div': 'authors', 'p': 'body'}
            """ wtf title error here 'http://abcnews.go.com/Politics/president-trumps-promises-point-busy-day-monday/story?id=44972708'""" 
        if ('wsj.com' in url):
            if ('To Read the Full Story,' in article_html_text):
                print('Article behind paywall for ' + url + ' . Skipping article. ')
                print("MUST DEBUG CONSISTENTLY")
                continue
            """ might be a lost cause""" 
            tags = {'title': [], 'span': ['name'], 'time': [], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'span': 'authors', 'time': 'date', 'p': 'body'}
        if ('marketwatch.com' in url):
            tags = {'title': [], 'div': ['first-author-has-dred'], 'p': ['timestamp'], 'p2': ['VANILLA']}
            nicknames = {'title': 'title', 'div': 'authors', 'p': 'date', 'p2': 'body'}
        if ('salon.com' in url):
            tags = {'title': [], 'span': ['byline'], 'span2': ['toLocalTime'], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'span': 'authors', 'span2': 'date', 'p': 'body'}
        if ('cnbc.com' in url):
            tags = {'title': [], 'div': ['source'], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'div': 'authors', 'p': 'body'}

            publish_date = url[url.find('telegraph.co') + len('telegraph.co'):]
            date_tokens = publish_date.split('/')
            year = date_tokens[1]
            month = date_tokens[2]
            day = date_tokens[3]
            d_cache = month + '-' + day + '-' + year
            date_cached = True
        if ('usatoday.com' in url):
            tags = {'title': [], 'span': ['asset-metabar-author asset-metabar-item'], 'span2': ['asset-metabar-time asset-metabar-item nobyline'], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'span': 'authors', 'span2': 'date', 'p': 'body'}
            #todo- remove , USA Today from end of autor
        if ('nationalreview.com' in url):
            tags = {'title': [], 'time': [], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'time': 'date', 'p': 'body'}
            author_cached = True
            #need to fix nested divs to get authors
        if ('vox.com' in url):
            tags = {'title': [], 'span': ['c-byline__item'], 'p':[]}
            nicknames = {'title': 'title', 'span': 'authors', 'p': 'body'}

            publish_date = url[url.find('vox.com') + len('vox.com'):]
            date_tokens = publish_date.split('/')
            year = date_tokens[2]
            month = date_tokens[3]
            day = date_tokens[4]
            d_cache = month + '-' + day + '-' + year
            date_cached = True
        if ('dailywire.com' in url):
            """ REMOVE LINE BELOW THIS- PLACEHOLDER TILL DIV FIXED. """
            article_html_text = article_html_text.replace('By:</div>', '')
            tags = {'title': [], 'div': ['field-label'], 'div2': ['field-published-on'], 'p': ['VANILLA']}
            nicknames = {'title': 'title', 'div': 'authors', 'div2': 'date', 'p': 'body'}


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
        if (body_cached is False and len(output_text['body']) > 3):
            """ This number is arbitrary- purely done to stop The HIll from doing weird shit """
            b_cache = output_text['body']
            body_key = reverse_nicknames['body']
            tags.pop(body_key)
            nicknames.pop(body_key)
            body_cached = True
        if (extra_cached is False and output_text['extra'] != []):
            e_cache = output_text['extra']
            extra_key = reverse_nicknames['extra']
            tags.pop(extra_key)
            nicknames.pop(extra_key)
            extra_cached = True


        """ Ensure it doesn't do that stupid bug where randomly shit
        isn't returned in request text. """
        while (title_cached is False or
               date_cached is False or
               author_cached is False or
               body_cached is False or
               extra_cached is False):
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
            if (body_cached is False and len(output_text['body']) > 3):
                b_cache = output_text['body']
                body_key = reverse_nicknames['body']
                tags.pop(body_key)
                nicknames.pop(body_key)
                body_cached = True
            if (extra_cached is False and output_text['extra'] != []):
                e_cache = output_text['extra']
                extra_key = reverse_nicknames['extra']
                tags.pop(extra_key)
                nicknames.pop(extra_key)
                extra_cached = True

        """ ugh, need to organize handlers- here we handle any weird cases
        of titles or authors containing stupid text on the end """
        if ('nytimes.com' in url):
            t_cache[0] = t_cache[0].replace(' - The New York Times', '')
        if ('politico.com' in url):
            d_cache = d_cache[:8]
            d_cache = d_cache.replace("/", "-")
            """ sometimes this above line an error... why..... makes it a list. """
            b_cache = [item for item in b_cache if 'AP Photo' not in item]
        if ('time.com' in url):
            if ('AM' in d_cache[0] or 'PM' in d_cache[0]):
                """ If TIME gives date published in their html as a specific time, it was published today. """
                d_cache = time.strftime("%m-%d-%Y")
            a_cache = [author.replace(' / AP', '') for author in a_cache]
        if ('thehill.com' in url):
            b_cache = [para for para in b_cache if "discussion thread." not in para and
                                                   "The Hill" not in para and
                                                   "The contents of this site" not in para and
                                                   "SPONSORED" not in para]
            author = a_cache[0].replace('By ', '')
            author = author[:author.find(' - ')]
            a_cache[0] = author
            t_cache[0] = t_cache[0].replace(' | TheHill', '')
            d_cache = d_cache[:8].replace('/', '-')
        if ('huffingtonpost.com' in url):
            t_cache[0] = t_cache[0].replace(' | The Huffington Post', '')
            d_cache = d_cache[:8].replace('/', '-')
            b_cache = [para for para in b_cache if "Learn more" not in para]
        if ('bloomberg.com' in url):
            d_cache = d_cache[:d_cache.find("</noscript>")]
            d_cache = remove_brackets(d_cache)
            d_cache = d_cache[:d_cache.find("2017") + 4]
            d_cache = d_cache.replace(" ", "-")
            d_cache = d_cache.replace(",", "")
            a_cache = [remove_brackets(author) for author in a_cache]
            a_cache = [author[:author.find('@')] for author in a_cache]
            b_cache = [para for para in b_cache if '<aside class="inline-newsletter" data-state="ready">' not in para]
            t_cache[0] = t_cache[0].replace(' - Bloomberg', '')
        if ('thedailybeast.com' in url):
            t_cache[0] = t_cache[0].replace(' - The Daily Beast', '')
            a_cache = remove_brackets(b_cache.pop(0))
            a_cache = a_cache[3:]
            a_cache = a_cache.split('and')
            a_cache = [author.strip() for author in a_cache]
        if ('heritage.org' in url):
            """ NEED TO FIX PARAGRAPH SHIT"""
            a_cache = [author.replace('By ', '') for author in a_cache]
            d_cache = d_cache[:d_cache.find(' |')]
            d_cache = d_cache.replace(',', '')
            d_cache = d_cache.replace(' ', '-')
            d_cache = d_cache.replace('</p', '')
            d_cache = d_cache.replace('<p>', '')
            b_cache = [para for para in b_cache if 'The Heritage Foundation' not in para and
                                                   '|' not in para and
                                                   'Contact Us' not in para and
                                                   'Privacy Policy' not in para]
        if ('theguardian.com' in url):
            t_cache[0] = (t_cache[0])[:t_cache[0].find('|')]
            b_cache2 = []
            for para in b_cache:
                if 'Before you post, we’d like to thank you for joining the debate' in para:
                    break
                b_cache2.append(para)
            b_cache = b_cache2
        if ('latimes.com'in url):
            t_cache[0] = t_cache[0].replace(' - LA Times', '')
        if ('telegraph.co' in url):
            b_cache = [para for para in b_cache if 'your internet connection' not in para and
                                                   'Telegraph Media Group Limited' not in para and
                                                   'we rely on revenue generated by advertising' not in para and
                                                   'Just a couple of clicks will make a big difference' not in para and
                                                   para != 'Thank you.' and
                                                   'for instructions' not in para]
        if ('thinkprogress.org' in url):
            b_cache = [para for para in b_cache if 'Moving news forward.' not in para and
                                                   'Contact me:' not in para]
            """ NEED MEANS TO DEAL WITH THEIR STUPID ARTIFICATS IN THE TEXT. """
            """ NEED TO HAVE HANDLER FOR X HOURS AGO AND Y DAYS AGO. """
        if ('nbcnews.com' in url):
            d_cache = d_cache[:d_cache.find(',')]
            d_cache = d_cache.replace(' ', '-')
        if ('cato.org' in url):
            """ finding the end is annoying it seems- need further testing of extractor. """
            t_cache[0] = t_cache[0].replace(' | Cato Institute', '')
            a_cache[0] = a_cache[0].replace('By ', '')
            a_cache[0] = a_cache[0][:a_cache[0].find('</div>')]
            a_cache = a_cache[0].split('and')
            d_cache = d_cache.replace(',', '')
            d_cache = d_cache.replace(' ', '-')
            d_cache = month_name_to_number(d_cache)
            b_cache = [para for para in b_cache if 'Unported License' not in para]
            quals = b_cache.pop(-1)
        if ('apnews.com' in url):
            a_cache[0] = a_cache[0].replace('By', '')
            a_cache = a_cache[0].split('and')
            """ Need mechanism for articles published close to midnight... add handler later"""
            if (('minutes ago' in d_cache) or ('hours ago' in d_cache) or ('Today' in d_cache)):
                d_cache = time.strftime("%m-%d-%Y")
            b_cache = [para for para in b_cache if "FILE" not in para]
        if ('abcnews.com' in url):
            t_cache[0] = t_cache[0].replace(' - ABC News', '')
        if ('marketwatch.com' in url):
            author = a_cache[0].split('<b>')
            author[1] = author[1][:author[1].find('</b>')]
            author[0] = author[0].replace('By', '')
            author[0] = remove_brackets(author[0]).replace('\r', '')
            a_cache = [author[0] + ' ' + author[1]]
            t_cache[0] = t_cache[0].replace(' - MarketWatch', '')
            b_cache.pop(0)
            b_cache.pop(0)
            b_cache.pop(-1)
            b_cache.pop(-1)
            b_cache.pop(-1)
            b_cache = [para for para in b_cache if 'This story was first published on 'not in para and
                                                    len(para) > 16]
            d_cache = remove_brackets(d_cache)
            d_cache = d_cache.replace('Published: ', '')
            d_cache = d_cache[:d_cache.find(':') - 2]
            d_cache = d_cache.replace(',', '')
            d_cache = d_cache.replace(' ', '-')
            d_cache = month_name_to_number(d_cache)
        if ('cnbc.com' in url):
            for i in range(7):
                b_cache.pop(-1)
            a_cache[0] = a_cache[0][:a_cache[0].find('</a>')]

            """ Need to removeblank lines in text... due to using '\r' in the text"""
            """ has artifcating of Â """
        if ('salon.com' in url):
            a_cache = [a_cache[-1]]
            t_cache[0] = t_cache[0].replace(' - Salon.com', '')
            d_cache = d_cache[(d_cache.find(',') + 2):]
            d_cache = d_cache[:(d_cache.find(':') - 2)].strip()
            d_cache = d_cache.replace(',', '')
            d_cache = d_cache.replace(' ', '-')
        if ('usatoday.com' in url):
            d_cache = d_cache[d_cache.find("ET") + 3:d_cache.find('|')].strip()
            d_cache = d_cache.replace(',', '')
            d_cache = d_cache.replace('.', '')
            d_cache = d_cache.replace(' ', '-')
            b_cache = [para for para in b_cache if 'USA TODAY NETWORK' not in para and
                                                   'Check out a new episode' not in para and
                                                   'Follow USA TODAY' not in para and
                                                   para != "We're sorry." and
                                                   para != "something went wrong."]
            a_cache[0] = a_cache[0][:a_cache[0].find('</a>')]
        if ('vox.com' in url):
            t_cache[0] = t_cache[0].replace(' - Vox', '')
            a_cache = [remove_brackets(a_cache[0][:a_cache[0].find('</a>')])]
            split_index = b_cache.index('Awesome, share it:')
            b_cache = b_cache[:split_index]
            b_cache[0] = b_cache[0][(b_cache[0].find('</figure>')):]
        if ('dailywire.com' in url):
            t_cache[0] = t_cache[0].replace(' | Daily Wire', '')
            b_cache.pop(0)
            for i in range(2):
                b_cache.pop(-1)
            a_cache = [a_cache[0]]
            d_cache = d_cache.replace(',', '')
            d_cache = d_cache.replace(' ', '-')
            d_cache = month_name_to_number(d_cache)


        if ('nationalreview.com' in url):
            t_cache[0] = t_cache[0].replace('  | National Review', '')
            a_cache = ['National Review']
            d_cache = remove_brackets(d_cache)
            d_cache = d_cache[:d_cache.find(':') - 2].strip()
            d_cache = d_cache.replace(',', '')
            d_cache = d_cache.replace(' ', '-')
            d_cache = month_name_to_number(d_cache)
            cite = a_cache[0] + ', ' + d_cache + ', "' + t_cache[0].strip() + '," ' + url
            #change to actual author when bug fixed
            #sometimes has quals, need to handle
        elif ('npr.org' in url):
            """ TO DO CHANGE ONCE FIGURE OUT AUTHOR APPROACH """
            t_cache[0] = (t_cache[0])[:t_cache[0].find(':')]
            d_cache = d_cache.replace(",", "")
            d_cache = d_cache.replace(' ', '-')
            d_cache = month_name_to_number(d_cache)
            b_cache = [para for para in b_cache if 'Get in touch with your questions, comments and leads.' not in para]
            cite = a_cache[0] + ', ' + d_cache + ', "' + t_cache[0].strip() + '," ' + url
        elif ('rt.com' in url):
            t_cache[0] = t_cache[0].replace(' — RT News', '')
            b_cache.insert(0, e_cache[0])
            d_cache = d_cache[d_cache.find("GMT,") + 5:]
            d_cache = d_cache.replace(",", "")
            d_cache = d_cache.replace(" ", "-")
            cite = a_cache[0] + ', ' + d_cache + ', "' + t_cache[0].strip() + '," ' + url
        elif ('cbsnews.com' in url):
            t_cache[0] = t_cache[0].replace(' - CBS News', '')
            d_cache = d_cache[:d_cache.find(',') + 6]
            d_cache = d_cache.replace(",", "")
            d_cache = d_cache.replace(" ", "-")
            d_cache = month_name_to_number(d_cache)
            cite = a_cache[0] + ', ' + d_cache + ', "' + t_cache[0].strip() + '," ' + url
        elif ('xinhuanet.com' in url):
            b_cache2 = []
            b_cache.pop(1)
            for para in b_cache:
                if 'Copyright ' in para:
                    break
                b_cache2.append(para)
            b_cache = b_cache2
            a_cache = 'Xinhua'
            cite = a_cache + ', ' + d_cache + ', "' + t_cache[0].strip() + '," ' + url
        elif ('dailykos.com' in url):
            b_cache = [para for para in b_cache if 'Kos Media, LLC.' not in para and
                                                   'is the author of' not in para and
                                                   'Return to edit' not in para]
            a_cache = 'Daily Kos'
            """ TODO REMOVE WHEN FIXED """
            cite = a_cache + ', ' + d_cache + ', "' + t_cache[0].strip() + '," ' + url
        elif ('foxnews.com' in url):
            t_cache[0] = t_cache[0].replace(' | Fox News', '')
            cite = a_cache + ', ' + d_cache + ', "' + t_cache[0].strip() + '," ' + url
            a_cache = html_wrapper(a_cache[0], {'p': []})
        else:
            """ Create author names. """
            a_cache = [remove_brackets(item) for item in a_cache]
            authors_last = ''
            authors_first = ''
            for author in a_cache:
                author_tokens = author.split()
                author_tokens = [author.replace(",", "") for author in author_tokens]
                if ((authors_last != '') and (a_cache.index(author) == (len(a_cache) - 1))):
                    if (len(a_cache) == 2):
                        authors_last += ' '
                        authors_first += ' '
                    authors_last += 'and '
                    authors_first += 'and '
                    authors_first += author_tokens[0].lower().capitalize()
                    authors_last += author_tokens[-1].lower().capitalize()
                else:
                    authors_first += author_tokens[0].lower().capitalize()
                    authors_last += author_tokens[-1].lower().capitalize()
                    if (len(a_cache) > 2):
                        authors_last += ', '
                        authors_first += ', '
            """ Need handler for hyphenated names- make capital afterwards """
            d_cache = month_name_to_number(d_cache)

            """ Create cite. """
            cite = authors_last.strip() + ', ' + d_cache + ', ' + authors_first.strip() + ', "' + t_cache[0].strip() + '," ' + url

        """ Create body. """
        body = b_cache
        text = ''
        for para in body:
            para = remove_brackets(para).strip()
            if ((para != '') and (para.replace(' ', '') != '')):
                text += (para + '\n')

        """ Card is cite + body. """
        card = cite + '\n\n' + text + '\n\n'

        """ Get rid of stupid html equivalent expressions (e.g. Fox uses the
        html code for quotation marks instead of just using quotes in the html). """
        card = remove_common_artifacts(card)

        f = open('card output', 'ab')

        """ Write card to output file."""
        f.write(card.encode('utf-8'))

        f.close()


def month_name_to_number(date):
    proper_names = {"January": 1,
                    "February": 2,
                    "March": 3,
                    "April": 4,
                    "May": 5,
                    "June": 6,
                    "July": 7,
                    "August": 8,
                    "September": 9,
                    "October": 10,
                    "November": 11,
                    "December": 12}
    for key in proper_names:
        date = date.replace(key, str(proper_names[key]))
    return date


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
    text = text.replace("&#x2019;", "'")
    text = text.replace('&#x201C;', '"')
    text = text.replace('&#x201D;', '"')
    text = text.replace('Â', '')
    text = text.replace("&rsquo;", "'")
    text = text.replace('&rdquo;', '"')
    text = text.replace('&ldquo;', '"')
    text = text.replace('“', '"')
    text = text.replace('”', '"')
    text = text.replace("’", "'")
    text = text.replace('&#8212;', '-')
    text = text.replace('—', '-')
    return text

#need a way to get rid of Â character. appears for seemingly no reason at times. 

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
