def html_searcher(text, tags, destructive=True):
    """
    >>> a, b = html_searcher('abcde', ['a'])
    >>> a
    []
    >>> b
    'abcde'
    >>> a2, b2 = html_searcher('<a href="http://www.nytimes.com/topic/person/donald-trump?inline=nyt-per" title="More articles about Donald J. Trump." class="meta-per">Donald J. Trump</a>', ['a'])
    >>> a2[0]
    'Donald J. Trump'
    >>> b2
    ''
    >>> a3, b3 = html_searcher('<a href="http://www.nytimes.com/topic/person/donald-trump?inline=nyt-per" title="More articles about Donald J. Trump." class="meta-per">Donald J. Trump</a>', ['q'])
    >>> a3
    []
    >>> b3
    '<a href="http://www.nytimes.com/topic/person/donald-trump?inline=nyt-per" title="More articles about Donald J. Trump." class="meta-per">Donald J. Trump</a>'
    >>> a4, b4 = html_searcher('<a href="http://www.nytimes.com/topic/person/donald-trump?inline=nyt-per" title="More articles about Donald J. Trump." class="meta-per">Donald J. Trump>', ['a'])
    >>> a4
    []
    >>> b4
    '<a href="http://www.nytimes.com/topic/person/donald-trump?inline=nyt-per" title="More articles about Donald J. Trump." class="meta-per">Donald J. Trump>'
    >>> a5, b5 = html_searcher('<a href="http://www.nytimes.com/topic/person/donald-trump?inline=nyt-per" title="More articles about Donald J. Trump." class="meta-per">Donald J. Trump</a><a href="http://www.nytimes.com/topic/person/donald-trump?inline=nyt-per" title="More articles about Donald J. Trump." class="meta-per">Donald T. Trump</a>', ['a'])
    >>> a5[0]
    'Donald J. Trump'
    >>> a5[1]
    'Donald T. Trump'
    >>> b5
    ''
    >>> a6, b6 = html_searcher('<a href="http://www.nytimes.com/topic/person/donald-trump?inline=nyt-per" title="More articles about Donald J. Trump." class="meta-per">Donald J. Trump<a href="http://www.nytimes.com/topic/person/donald-trump?inline=nyt-per" title="More articles about Donald J. Trump." class="meta-per">Donald T. Trump</a>', ['a'])
    >>> a6[0]
    'Donald J. Trump<a href="http://www.nytimes.com/topic/person/donald-trump?inline=nyt-per" title="More articles about Donald J. Trump." class="meta-per">Donald T. Trump'
    >>> b6
    ''
    >>> a7, b7 = html_searcher('<a href="http://www.nytimes.com/topic/person/donald-trump?inline=nyt-per" title="More articles about Donald J. Trump." class="meta-per">Donald J. Trump</a>abcde>', ['a'])
    >>> a7[0]
    'Donald J. Trump'
    >>> b7
    'abcde'
    """
    #known issues
    #1) bug where weird shit happens if last character is not a '>'- just adding it to end fails since lops of any remaining text
    assert type(text) is str
    assert type(tags) is list
    contained_text = []
    baseline_tag = tags.pop(0)
    remaining_text = text
    baseline_start = '<' + baseline_tag
    potential_start_index = remaining_text.find(baseline_start)
    while (potential_start_index != -1) and (len(remaining_text) != 0):
        start_tag = ''
        cur_char = remaining_text[potential_start_index]
        i = 0
        while (cur_char != '>'):
            start_tag += cur_char
            i += 1
            cur_char = remaining_text[potential_start_index + i]
        start_tag += cur_char

        correct_start_tag = True
        for tag in tags:
            cur_class = 'class="' + tag + '"'
            if cur_class not in start_tag:
                correct_start_tag = False
                break
        if correct_start_tag:
            end_tag = '</' + baseline_tag + '>'
            end_index = remaining_text.find(end_tag)
            if end_index == -1:
                remaining_text = ''
                #find way to combine this and lower statement identical to it
            else:
                text_grabbed = remaining_text[(potential_start_index + len(start_tag)):end_index]
                contained_text.append(text_grabbed)
                remaining_text = remaining_text[(end_index + len(end_tag)):]
        else:
            remaining_text = remaining_text[(potential_start_index + len(start_tag)):]
    if destructive and (len(contained_text) > 0):
        return contained_text, remaining_text
    else:
        return contained_text, text

if __name__ == "__main__":
    import doctest
    doctest.testmod()