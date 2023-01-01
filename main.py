import requests
import square
import pygame
from bs4 import BeautifulSoup

ColorBlackText = (0, 0, 0)
ColorWhiteText = (255, 255, 255)
ColorEmpty = (43, 43, 43)


# Returns the maximum number of episodes over all seasons
def getLongestSeason():
    tempLongest = 0
    for season in range(len(ratingsArr)):
        if len(ratingsArr[season]) > tempLongest:
            tempLongest = len(ratingsArr[season])
    return tempLongest


# Generating text function
def textObjects(text, font, color=ColorBlackText):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


# Inputting IMDb tak and parsing the HTML content
show = input("Enter Show IMDb tag: ")
soup = BeautifulSoup(requests.get("https://www.imdb.com/title/" + show + "/episodes").text, "html.parser")

# Find the show name and number of seasons
numOfSeasons = int(soup.find(id="episode_top").text[7:])
showName = soup.find(itemprop="url").text

# Initialize size and ratings array
s = 50
ratingsArr = []

# Initialize highest, lowest, and average score values
highestRating = -1
lowestRating = 11
averageRating = 0
averageCount = 0

for season in range(numOfSeasons):
    # Parse HTML content from individual season pages
    soupSeason = BeautifulSoup(
        requests.get("https://www.imdb.com/title/" + show + "/episodes?season=" + str(season + 1)).text, "html.parser")

    # Gather all instances of ratings on page
    ratings = soupSeason.findAll(class_="ipl-rating-star small")

    # Set first item in each season row to the season number in a temporary array
    tempArr = [square.Square(season + 1, s, ColorEmpty)]

    # Go through each item in the ratings parsed content
    for rating in ratings:
        # Add each rating individually to the end of the temporary array
        tempArr.append(square.Square(float(rating.text[8:11]), s))

        # Functions for determining if the currently selected rating is the highest or lowest
        if float(rating.text[8:11]) > highestRating:
            highestRating = float(rating.text[8:11])
        elif float(rating.text[8:11]) < lowestRating:
            lowestRating = float(rating.text[8:11])

        # Adding the current rating to the total alongside ratings count
        averageRating += float(rating.text[8:11])
        averageCount += 1
    # Add the temporary array as a part of the ratingsArr 2-dimensional array
    ratingsArr.append(tempArr)

# Find the most episodes in one season now that all the seasons have been added
numOfEpisodes = getLongestSeason()

# Fill in any empty spots in the array with -1 to make printing the grid easier
for season in range(numOfSeasons):
    for episode in range(numOfEpisodes):
        if len(ratingsArr[season]) < numOfEpisodes:
            for x in range(numOfEpisodes - len(ratingsArr[season])):
                ratingsArr[season].append(square.Square(-1, s))

# Resize the grid if there are more episodes / seasons
if getLongestSeason() > 30 or numOfSeasons > 10:
    s = 30
    for season in range(len(ratingsArr)):
        for episode in range(len(ratingsArr[season])):
            ratingsArr[season][episode].setWidth(s)

# Calculate average
averageRating /= averageCount

# Add a episode number row at the beginning of the array
tempArr = []
for episode in range(numOfEpisodes):
    tempArr.append(square.Square(episode, s, ColorEmpty))
ratingsArr.insert(0, tempArr)

# Pygame initializations
pygame.init()
pygame.display.set_caption('IMDb')
pygame.display.set_icon(pygame.image.load('IMDb.png'))

# Determining grid dimensions and pygame spacing
w, h = numOfEpisodes + 1, numOfSeasons + 1
border, topSpace = 6, (s * 1.25) + (s / 6)

# Set a minimum for the window width alongside auto adjusting window sizes
windowWidth = 0
if numOfEpisodes < 7:
    windowWidth = 600
else:
    windowWidth = s * 1.25 * w
windowHeight = s * 1.3 * h + topSpace
window = pygame.display.set_mode((windowWidth, windowHeight))

# Font initializations
regText = pygame.font.SysFont("Arial", int(s * 0.7))
boldText = pygame.font.SysFont("Arial-Bold", int(s * 0.85))

# Printing data in command line
print("Show name: " + showName)
print("Number of seasons: " + str(numOfSeasons))
print("Number of episodes per season: " + str(numOfEpisodes))
print()

for season in range(len(ratingsArr)):
    for episode in range(len(ratingsArr[season])):
        print(ratingsArr[season][episode].getNumber(), end="\t")
    print()

print("Highest = " + str(highestRating) + "\tLowest = " + str(lowestRating) + "\tAverage = " + str(
    round(averageRating, 1)))

running = True
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False

    surface = pygame.display.get_surface()

    # Set background color
    window.fill(ColorEmpty)

    # Generate grid dimensions
    gridLength = w * (s + border)
    gridHeight = h * (s + border)
    centerBuffer = (windowWidth - gridLength) / 2 + (s / 25)

    # Generate grid
    rect = [[0 for x in range(w)] for y in range(h)]
    for row in range(len(ratingsArr)):
        for col in range(len(ratingsArr[row])):
            # Add rectangle to array
            rect[row][col] = pygame.Rect(col * (s + border) + centerBuffer,
                                         row * (s + border) + border + (s / 4) + topSpace, s, s)
            # Create border for empty squares
            pygame.draw.rect(window, ratingsArr[row][col].getColor(), rect[row][col], width=0, border_radius=3)

    # Generate text on each grid square
    for row in range(len(ratingsArr)):
        for col in range(len(ratingsArr[row])):
            if ratingsArr[row][col].getNumber() > 0:
                if row > 0 and col > 0:
                    textSurf, textRect = textObjects(str(ratingsArr[row][col].getNumber()), regText)
                else:
                    textSurf, textRect = textObjects(str(ratingsArr[row][col].getNumber()), regText, ColorWhiteText)
            else:
                textSurf, textRect = textObjects("", regText)
            textRect.center = (rect[row][col].x + s / 2, rect[row][col].y + s / 2)
            window.blit(textSurf, textRect)

    # Highest label
    textSurf, textRectHighest = textObjects("H: ", regText, ColorWhiteText)
    textRectHighest.center = (windowWidth / 2, topSpace / 1.5)
    window.blit(textSurf, textRectHighest)

    # Highest square
    highestRect = pygame.Rect(textRectHighest.x + textRectHighest.width, textRectHighest.y - (s / 10), s, s)
    highestSquare = square.Square(highestRating, s)
    pygame.draw.rect(window, highestSquare.getColor(), highestRect, width=0, border_radius=3)

    # Highest square text
    textSurf, textRect = textObjects(str(highestSquare.getNumber()), regText)
    textRect.center = (highestRect.x + s / 2, highestRect.y + s / 2)
    window.blit(textSurf, textRect)

    # Show title
    textSurf, textRectShow = textObjects(showName, boldText, ColorWhiteText)
    textRectShow.center = (textRectHighest.x - textRectShow.width * 0.75, topSpace / 1.5)
    window.blit(textSurf, textRectShow)

    # Lowest label
    textSurf, textRectLowest = textObjects("L: ", regText, ColorWhiteText)
    textRectLowest.center = (highestRect.x + highestRect.width * 1.6, topSpace / 1.5)
    window.blit(textSurf, textRectLowest)

    # Lowest square
    lowestRect = pygame.Rect(textRectLowest.x + textRectLowest.width, textRectLowest.y - (s / 10), s, s)
    lowestSquare = square.Square(lowestRating, s)
    pygame.draw.rect(window, lowestSquare.getColor(), lowestRect, width=0, border_radius=3)

    # Lowest square text
    textSurf, textRect = textObjects(str(lowestSquare.getNumber()), regText)
    textRect.center = (lowestRect.x + s / 2, lowestRect.y + s / 2)
    window.blit(textSurf, textRect)

    # Average label
    textSurf, textRectAverage = textObjects("Avg: ", regText, ColorWhiteText)
    textRectAverage.center = (lowestRect.x + lowestRect.width * 1.85, topSpace / 1.5)
    window.blit(textSurf, textRectAverage)

    # Average square
    averageRect = pygame.Rect(textRectAverage.x + textRectAverage.width, textRectAverage.y - (s / 10), s, s)
    averageSquare = square.Square(round(averageRating, 1), s)
    pygame.draw.rect(window, averageSquare.getColor(), averageRect, width=0, border_radius=3)

    # Average square text
    textSurf, textRect = textObjects(str(averageSquare.getNumber()), regText)
    textRect.center = (averageRect.x + s / 2, averageRect.y + s / 2)
    window.blit(textSurf, textRect)

    pygame.display.flip()
