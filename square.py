ColorOutstanding = (0, 176, 80)  # 9.6-10
ColorVeryGood = (146, 208, 80)  # 9-9.5
ColorGood = (255, 255, 0)  # 8-8.9
ColorModerate = (255, 192, 0)  # 7-7.9
ColorBad = (255, 0, 0)  # 0-6.9
ColorEmpty = (43, 43, 43)  # Empty (-1)


# Determine color by number
def determineColor(number):
    if number > 9.5:
        return ColorOutstanding
    elif number > 8.9:
        return ColorVeryGood
    elif number > 7.9:
        return ColorGood
    elif number > 6.9:
        return ColorModerate
    elif number > 0:
        return ColorBad
    else:
        return ColorEmpty


class Square:
    def __init__(self, number=0, width=0, color=0):
        self.number = number
        self.width = width

        # Determine color based on number if not specified in constructor
        if color == 0:
            self.color = determineColor(number)
        else:
            self.color = color

    def setWidth(self, width):
        self.width = width

    def setNumber(self, number):
        self.number = number

    def getWidth(self):
        return self.width

    def getNumber(self):
        return self.number

    def getColor(self):
        return self.color
