def html_searcher(text, tags, destructive=True):
    """
    >>> a, b = html_searcher('abcde', ['a'])
    >>> a
    []
    >>> b
    'abcde'
    >>> a2, b2 = html_searcher('<a class="meta-per">Donald J. Trump</a>', ['a'])
    >>> a2[0]
    'Donald J. Trump'
    >>> b2
    ''
    >>> a3, b3 = html_searcher('<a class="meta-per">Donald J. Trump</a>', ['q'])
    >>> a3
    []
    >>> b3
    '<a class="meta-per">Donald J. Trump</a>'
    >>> a4, b4 = html_searcher('<a class="meta-per">Donald J. Trumpa</a', ['a'])
    >>> a4
    []
    >>> b4
    '<a class="meta-per">Donald J. Trumpa</a'
    >>> a5, b5 = html_searcher('<a class="meta-per">Donald J. Trump</a><a class="meta-per">Donald T. Trump</a>', ['a'])
    >>> a5[0]
    'Donald J. Trump'
    >>> a5[1]
    'Donald T. Trump'
    >>> b5
    ''
    >>> a6, b6 = html_searcher('<aclass="meta-per">Donald J. Trump<a class="meta-per">Donald T. Trump</a>', ['a'])
    >>> a6[0]
    'Donald J. Trump<a class="meta-per">Donald T. Trump'
    >>> b6
    ''
    >>> a7, b7 = html_searcher('<a class="meta-per">Donald J. Trump</a>abcde>', ['a'])
    >>> a7[0]
    'Donald J. Trump'
    >>> b7
    'abcde>'
    >>> a8, b8 = html_searcher('<a>a</a><a>b</a><a>c</a><a>d</a><a>e</a>', ['a'])
    >>> a8[0]
    'a'
    >>> a8[4]
    'e'
    >>> b8
    ''
    >>> a9, b9 = html_searcher('<a><b>a</b></a>', ['a'])
    >>> a9[0]
    '<b>a</b>'
    >>> a10, b10 = html_searcher('<a>a</a><a class="q">b</a>', ['a', 'q'])
    >>> len(a10)
    1
    >>> a10[0]
    'b'
     >>> a11, b11 = html_searcher('<a class="meta-per">Donald J. Trump</a>', ['a', 'meta-per'])
    >>> a11[0]
    'Donald J. Trump'
    >>> b11
    ''
    """
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
        if (len(tags) != 0 and tags[0] == 'VANILLA'):
            correct_start_tag = (start_tag == baseline_start + '>')
        else:
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
            else:
                text_grabbed = remaining_text[(potential_start_index + len(start_tag)):end_index]
                contained_text.append(text_grabbed.strip().replace('    ', '').replace('\n', ''))
                remaining_text = remaining_text[(end_index + len(end_tag)):]
        else:
            remaining_text = remaining_text[(potential_start_index + len(start_tag)):]
        potential_start_index = remaining_text.find(baseline_start)
    contained_text = [x for x in contained_text if x != '']
    if destructive and (len(contained_text) > 0):
        return contained_text, remaining_text
    else:
        return contained_text, text


def html_wrapper(text, blocks_to_find, nicknames={}):
    """
    >>> html_wrapper('<a class="b">abcde</a>', {'a': ['b']})
    {'a': ['abcde']}
    >>> html_wrapper('<a class="b">abcde</a>', {'a': ['b']}, {'a': 'body'})
    {'body': ['abcde']}
    """
    output_dict = {}
    for key in blocks_to_find:
        if key[-1] in '0123456789':
            cur_tags = [key[:-1]] + blocks_to_find[key]
        else:
            cur_tags = [key] + blocks_to_find[key]
        output, text = html_searcher(text, cur_tags)
        if (nicknames != {}):
            output_dict[nicknames[key]] = output
        else:
            output_dict[key] = output
    return output_dict


if __name__ == "__main__":
    import doctest
    doctest.testmod()
