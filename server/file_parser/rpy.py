from enum import Enum


class LineType(Enum):
    SRC = 1
    TRANS = 2
    OTHER = 3


class FileTextFlow:
    def __init__(self, id, src, trans) -> None:
        self.id = id
        self.src = src
        self.trans = trans

    def __repr__(self) -> str:
        return "id:{}, src:{}, trans:{}".format(self.id, self.src, self.trans)


class RpyLine:
    def __init__(self, id=0, content=""):
        self.id = id
        self.type = self.get_type(content)
        self.content = content

    def get_type(self, line_str):
        line_str_strip = line_str.strip()
        if line_str_strip == '':
            return LineType.OTHER
        if line_str[0] == ' ':
            if line_str_strip[0] == '#':
                if len(line_str_strip) >= 6 and line_str_strip[1:6] == ' game':
                    return LineType.OTHER
                elif len(line_str_strip) >= 7 and line_str_strip[1:7] == ' voice':
                    return LineType.OTHER
                elif len(line_str_strip) >= 11 and line_str_strip[1:11] == ' nvl clear':
                    return LineType.OTHER
                else:
                    return LineType.SRC
            elif len(line_str_strip) >= 3 and line_str_strip[0:3] == 'old':
                return LineType.SRC
            elif len(line_str_strip) >= 5 and line_str_strip[0:5] == 'voice':
                return LineType.OTHER
            elif len(line_str_strip) >= 9 and line_str_strip[:9] == 'nvl clear':
                return LineType.OTHER
            else:
                return LineType.TRANS
        else:
            return LineType.OTHER
    
    def __repr__(self) -> str:
        return '{}:{}'.format(self.id, self.content)


class RpyFile:
    def __init__(self, file_name, encoding="utf-8"):
        self.rpy_lines = []
        with open(file_name, encoding=encoding) as rpy_file:
            lines = rpy_file.readlines()
            for i in range(len(lines)):
                rpy_line = RpyLine(i, lines[i].rstrip())
                self.rpy_lines.append(rpy_line)
    
    def get_text_flows(self):
        src_lst = []
        trans_lst = []
        for rpy_line in self.rpy_lines:
            if  rpy_line.type == LineType.SRC:
                content = ""
                if rpy_line.content.strip()[0] == '#':
                    content = rpy_line.content.strip()[1:].strip()
                else:
                    content = rpy_line.content.strip()[3:].strip()
                src_lst.append(content)
            if rpy_line.type == LineType.TRANS:
                trans_lst.append(rpy_line.content.strip())
        if len(src_lst) != len(trans_lst):
            raise ValueError("length of src_lst and trans_lst are not equal!")
        res = []
        for i in range(len(src_lst)):
            tf = FileTextFlow(i, src_lst[i], trans_lst[i])
            res.append(tf)
        return res


if __name__ == '__main__':
    rf = RpyFile("../HB-DLC/HB-DLC/script/scene1-cactus.rpy", "utf-8-sig")
    tfs = rf.get_text_flows()
    for tf in tfs:
        print(tf)
