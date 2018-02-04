import platform
import json
import re
import subprocess

import solargraph_utils as solar
from deoplete.util import getlines,expand
from .base import Base

is_window = platform.system() == "Windows"

class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)
        self.name = 'solargraph'
        self.filetypes = ['ruby']
        self.mark = '[solar]'
        self.rank = 900
        self.input_pattern = r'\.[a-zA-Z0-9_?!]*|[a-zA-Z]\w*::\w*'
        self.is_server_started = False

    def on_init(self, context):
        vars = context['vars']
        self.encoding = self.vim.eval('&encoding')

        self.command = expand(vars.get('deoplete#sources#solargraph#command', 'solargraph'))
        self.args = vars.get('deoplete#sources#solargraph#args', ['--port', '0'])

    def start_server(self):
        if self.is_server_started == True:
            return True

        if not self.command:
            self.print_error('No solargraph binary set.')
            return

        if not self.vim.call('executable', self.command):
            return False

        try:
            self.server = solar.Server()
        except solar.ServerException as error:
            self.print_error(str(error))
            return False

        self.client = solar.Client(self.server.url)
        self.is_server_started = True
        return True

    def get_complete_position(self, context):
        m = re.search('[a-zA-Z0-9_?!]*$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        if not self.start_server():
            return []

        line = context['position'][1] - 1
        column = context['complete_position']
        text = '\n'.join(getlines(self.vim)).encode(self.encoding)
        filename = self.get_absolute_filepath()

        result = self.client.suggest(text=text, line=line, column=column, filename=filename)

        if result['status'] != 'ok':
            return []

        output = result['suggestions']

        return [{
            'word': cand['insert'],
            'kind': cand['kind'],
            'dup': 1,
            'abbr': self.build_abbr(cand),   # in popup menu instead of 'word'
            'info': cand['label'],  # in preview window
            'menu': cand['detail'], # after 'word' or 'abbr'
        } for cand in result['suggestions']]

    def build_abbr(self, cand):
        abbr = cand['label']
        kind = cand['kind']

        if kind == 'Method':
            args = ', '.join(cand['arguments'])
            abbr += '({})'.format(args)

        return abbr

    def get_absolute_filepath(self):
        path = self.vim.call('expand', '%:p')
        if len(path) == 0:
            return None
        return path
