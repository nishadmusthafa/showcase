
class SpecialSyntaxTranslator(object):
    def __init__(self):
        self.input = ''
        self.context = ''
        self.enquote = False
        self.output = ''

    def set_input(self, input_string):
        self.input = input_string

    def enquote_strings(self):
        self.enquote = True

    def unenquote_strings(self):
        self.enquote = False

    def translate_special_syntax(self):
        # For this implementation(talkdesk challenge), I'm assuming a basic parser of the %% syntax. 
        # Eg: "escape sequences" are not being implemented currently.
        # So if you use % within a variable, this function would fail. This is a TODO
        # if target_string = "the%sample%budapest%sample2%"
        # and context = {'sample': grand, '*', 'hotel'}
        # the return value is "thegrandbudapesthotel"
        # * is like a 'default' fallback. If there is no
        # replacement found, then the string is not translated and
        # returned as is. 
        variable_found = False
        variable = ""
        self.output = ''
        for char in self.input:
            if not char == "%":
                if variable_found:
                    variable += char
                else:
                    self.output += char
            else:
                variable += char
                if variable_found:
                    if variable[1:-1] in self.context:
                        translated_string = self.context[variable[1:-1]]
                    elif '*' in self.context:
                        translated_string = self.context['*']
                    else:
                        translated_string = variable
                    if self.enquote:
                        translated_string = "\"" + translated_string + "\""
                    self.output += translated_string
                    variable = ""
                variable_found = not variable_found

    def flatten_and_build(self, info):
        result = {}
        for key in info.keys():
            if type(info[key]) is dict:
                for child_key, value in self.flatten_and_build(info[key]).iteritems():
                    result[key + "." + child_key] = value
            else:
                result[key] = info[key]
        return result

    def build_context(self, info):
        self.context = self.flatten_and_build(info)




