from pygame import font


class EndScreenFont:
    __FONT_RATIO = 14.5

    def __init__(self):
        self.font = font.SysFont("Roboto", 15, bold=True)

    def update_font(self, height: int):
        size = int(height // self.__FONT_RATIO)
        self.font = font.SysFont("arialblack", size)

    def pause_text_size(self, text: str) -> tuple[int, int]:
        width, height = self.font.size(text)
        return width, height


"""
['arial', 'arialblack', 'bahnschrift', 'calibri', 'cambria', 'cambriamath', 'candara', 'comicsansms', 'consolas', 
'constantia', 'corbel', 'couriernew', 'ebrima', 'franklingothicmedium', 'gabriola', 'gadugi', 'georgia', 'impact', 
'inkfree', 'javanesetext', 'leelawadeeui', 'leelawadeeuisemilight', 'lucidaconsole', 'lucidasans', 'malgungothic', 
'malgungothicsemilight', 'microsofthimalaya', 'microsoftjhenghei']
"""
