def write_title(buffer, title, line_length=80):
    buffer.write('# {} {}\n'.format(title,
                                    '#' * (line_length - len(title) - 4)))
