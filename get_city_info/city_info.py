# encoding:utf8

class city_info:

    id = 0
    
    def __init__(self, id=None, code=None, name=None, parent_id=None, url=None, level=0):
        self.id=id
        self.level = level
        self.name = name
        self.parent_id = parent_id
        self.url = url
        if isinstance(code, int):
            self._code = ('%012d'%int(str(code)[::-1]))[::-1]
        elif isinstance(code, str):
            if len(code)>=12:
                self._code = code
            else:
                self._code = ('%012d'%int(code[::-1]))[::-1]
        else:
            self._code=''
            
    def set_info(self, input_str):
        if input_str is None or not isinstance(input_str, str) or input_str.strip() == '':
            return
        attrs = ['id', 'code', 'name', 'level', 'parent_id', 'url']
        input_list = input_str.strip().split()
        for i in range(len(input_list)):
            exec('self.%s = \'%s\''%(attrs[i], input_list[i]))
        if self.id is not None:
            if isinstance(self.id, str) and self.id != '':
                self.id = int(self.id)

        if self.level is not None:
            if isinstance(self.level, str) and self.level != '':
                self.level = int(self.level)
        
        if self.parent_id is not None:
            if isinstance(self.parent_id, str) and self.parent_id != '':
                self.parent_id = int(self.parent_id)


    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        if isinstance(code, int):
            self._code = ('%012d'%int(str(code)[::-1]))[::-1]
        elif isinstance(code, str):
            if len(code)>=12:
                self._code = code
            else:
                self._code = ('%012d'%int(code[::-1]))[::-1]

    def __str__(self):
        output_str = ''
        if self.id is None:
            output_str+='\t'
        else:
            output_str+=str(self.id)+'\t'
        if self.code is None:
            output_str+='\t'
        else:
            output_str+=str(self.code)+'\t'
        if self.name is None:
            output_str+='\t'
        else:
            output_str+=str(self.name)+'\t'
        if self.level is None:
            output_str+='\t'
        else:
            output_str+=str(self.level)+'\t'
        if self.parent_id is None:
            output_str+='\t'
        else:
            output_str+=str(self.parent_id)+'\t'
        
        return output_str.strip()