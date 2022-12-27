import requests
from bs4 import BeautifulSoup
#https://www.imdb.com/title/tt9253284/episodes

# Parse the HTML content
show = "tt0096697"
soup = BeautifulSoup(requests.get("https://www.imdb.com/title/" + show + "/episodes").text, "html.parser")

# Find the first <h1> element
numOfSeasons = int(soup.find(id="episode_top").text[7:])
showName = soup.find(itemprop="url").text
numOfEpisodes = int(soup.find(itemprop="numberofEpisodes").get("content"))

ratingsArr = []
for season in range(numOfSeasons):
    soupSeason = BeautifulSoup(requests.get("https://www.imdb.com/title/" + show + "/episodes?season=" + str(season + 1)).text, "html.parser")
    ratings = soupSeason.findAll(class_="ipl-rating-star small")
    tempArr = []
    for rating in ratings:
        tempArr.append(rating.text[8:11])
    ratingsArr.append(tempArr)


# Print the text
print("Show name: " + showName)
print("Number of seasons: " + str(numOfSeasons))
print("Number of episodes per season: " + str(numOfEpisodes))
print()
print("", end="\t")
for x in range(numOfEpisodes):
    print(str(x + 1), end="\t")
print()

for season in range(len(ratingsArr)):
    print(str(season + 1), end="\t")
    for episode in range(len(ratingsArr[season])):
        print(ratingsArr[season][episode], end="\t")
    print()