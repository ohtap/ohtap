import json
import os

import textract

# (1) Find all the files that this script should parse.
#     In this case, it's all .docx files in the SOK collections.

docx_files = [filename for filename in os.listdir('data')
              if filename.startswith('SOK_') and filename.endswith('.docx')]
for filename in docx_files:
    docname = filename[:-5]  # We already know the extension is ".docx"
    text = textract.process(os.path.join('data', filename)).decode()
    lines = [line.strip() for line in text.split('\n') if len(line)]

    # The files are in this format:
    # Title page
    # Metadata
    # Introduction
    # Interview
    # The Metadata, Introduction, and Interview sections all start with the header which contains
    # a line that is excatly "Spotlighting Oklahoma." These are the last three indexes the word
    # is found in. The title page may also have 'Spotlighting Oklahoma' appearing on its own line.
    # However, we simply use the last three. It's very unlikely that in the last three sections,
    # the phrase "Spotlighting Oklahoma" appears on its own line. It may appear in a sentence, but
    # it shouldn't be its own line.
    header_idxs = [i for i, val in enumerate(lines) if val == 'Spotlighting Oklahoma']
    metadata_lines = lines[header_idxs[-3]:header_idxs[-2]]
    introduction_lines = lines[header_idxs[-2]:header_idxs[-1]]
    interview_lines = lines[header_idxs[-1]:]

    # We'll focus on the main task of parsing the interview lines. There's not too much to parse
    # from the header, metadata, and introduction, though they do also contain useful information.
    # Those are items that I might call "sections" under my parsing scheme.
    section_id = 2  # Magical constant for now: The interview is the third section
    statement_id = -1
    current_statement = None
    statement_text = ''
    statements = list()
    for line in interview_lines:
        # A new statement starts with the speaker's name, then a tab, then the content.
        # I assume that tabs are only found in this context.
        if '\t' in line:
            # Consider that the "current statement" we were just working on is now done.
            # It's now the previous statement, and we start a new one. Unless this is the
            # very first statement, in which case the previous statement is None, we now
            # add it to our list of statements. And then work on a new one.
            if statement_id >= 0:
                statements.append(current_statement)
            statement_id += 1
            current_statement = {
                'id': '%s-%d-%d' % (docname, section_id, statement_id),
                'speaker': '',
                'text': ''}
            name, text = line.split('\t')
            current_statement['speaker'] = name.strip()
            current_statement['text'] += text.strip()
        elif statement_id >= 0:
            # This line represents a new paragraph resulting from a line break in the
            # same statement as the previous line, a continuation from the previous
            # line.
            current_statement['text'] += line
        else:
            # This means statement_id = -1, which means we have not started the first
            # statement yet.
            continue
    # Make sure to append the last statement we were working on when we exit the loop!
    statements.append(current_statement)


    with open(os.path.join('data', '%s.json' % docname), 'w') as f:
        json.dump(statements, f)

