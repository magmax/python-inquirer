# -*- coding: utf-8 -*-

from . import Text


class Path(Text):
    def get_header_template(self):
        return self.theme.text.template_for_title
