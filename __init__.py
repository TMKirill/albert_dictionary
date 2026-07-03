import re
import os
from pathlib import Path

from albert import *

md_iid = "5.0"
md_version = "1.0.0"
md_name = "Dictionary"
md_description = "Interface for dict.cc based dictionaries"
md_authors = ["TMK"]

class Plugin(PluginInstance, GeneratorQueryHandler):

    dictionaries_path = Path(__file__).parent/"dictionaries/"
    dict_cc_url = "https://my.dict.cc/"

    def __init__(self):
        PluginInstance.__init__(self)
        GeneratorQueryHandler.__init__(self)
        self._basic_reg_exp = self.readConfig("basic_reg_exp", str) or '^%s\\b'
        self.lines = []
        self.dictionaries = []
        dictionaries_directory_content = os.scandir(Plugin.dictionaries_path)
        if dictionaries_directory_content:
            for entry in dictionaries_directory_content:
                if entry.is_file() and entry.name.endswith('.txt'):
                    dictionary_name = entry.name.replace('.txt', '')
                    self.dictionaries.append(dictionary_name)

    def defaultTrigger(self):
        return 'dict '
    
    @property
    def basic_reg_exp(self):
        return self._basic_reg_exp
    
    @basic_reg_exp.setter
    def basic_reg_exp(self, value):
        self._basic_reg_exp = value
        self.writeConfig("basic_reg_exp", value)
    
    def configWidget(self):
        return [
            {
                "type": "lineedit",
                "label": "Basic regular expression",
                "property": "basic_reg_exp",
                "widget_properties": {"placeholderText": "^%s\\b"}
            },
            {
                "type": "label",
                "text": "<a href=\"file://%s\">Dictionaries directory</a>" % Plugin.dictionaries_path,
            },
            {
                "type": "label",
                "text": "<a href=\"%s\">Learn about dict.cc</a>" % Plugin.dict_cc_url,
            },

        ]
    
    def getLinesFromDictionary(self, dictionary):
        with open(Plugin.dictionaries_path/(dictionary + ".txt"), 'r') as fp:
            return fp.readlines()
    
    def items(self, ctx):
        items = []
        query = ctx.query
        if not query:
            if self.dictionaries:
                for dictionary_name in self.dictionaries:
                        items.append(
                            StandardItem(
                                id=self.id(),
                                text=dictionary_name,
                                input_action_text=dictionary_name + ' '
                            )
                        )
                yield items
            else:
                yield [StandardItem(id=self.id(),
                    text="There is no dictionaries")]
        else:
            query = query.split(' ', 1)
            dictionary = query[0]
            word = query[1].strip().lower()
            is_common_search = True
            if word.startswith('\\ '):
                word = word.replace('\\ ', '')
                is_common_search = False
            if word:
                answers = []
                lines = self.getLinesFromDictionary(dictionary)
                for row in lines:
                    row_lower = row.lower()
                    search_expression = ''
                    if is_common_search:
                        search_expression = self._basic_reg_exp % word
                    else:
                        search_expression = word
                    if re.search(search_expression, row_lower):
                        answers.append(row)
                if answers:
                    items = []
                    for answer in answers[::-1]:
                        pair = answer.replace('\n','').split('\t', 1)
                        answer = pair[0] + ' - ' + pair[1]
                        items.append(
                            StandardItem(
                                id=self.id(),
                                text=answer,
                            )
                        )
                    yield items
                else:
                    yield [StandardItem(id=self.id(),
                        text="No matches found")]
            else:
                yield [StandardItem(id=self.id(),
                    text="Enter the word to start search")]
        return