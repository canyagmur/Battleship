from prompt_toolkit import prompt

text = prompt('Give me some input: ')
print('You said: %s' % text)


from prompt_toolkit import PromptSession

# Create prompt object.
session = PromptSession()

# Do multiple input calls.
text1 = session.prompt()
text2 = session.prompt()



"""Coloring the prompt itself"""

from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style

style = Style.from_dict({
    # User input (default text).
    '':          '#ff0066',

    # Prompt.
    'username': '#884444',
    'at':       '#00aa00',
    'colon':    '#0000aa',
    'pound':    '#00aa00',
    'host':     '#00ffff bg:#444440',
    'path':     'ansicyan underline',
})

message = [
    ('class:username', 'can'),
    ('class:at',       '@'),
    ('class:host',     'localhost'),
    ('class:colon',    ':'),
    ('class:path',     '/user/can'),
    ('class:pound',    '# '),
]

text = prompt(message, style=style)

"""Autocompletion"""

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

html_completer = WordCompleter(['A1', 'A2', 'A3', 'A4'])
text = prompt('Enter HTML: ', completer=html_completer)
print('You said: %s' % text)

myship = '       _~      \n\
    _~ )_)_~   \n\
    )_))_))_)   DENEME 123\n\
    _!__!__!_   DENEME 123\n\
    \______t/  \n\
  ~~~~~~~~~~~~~'
print(myship)