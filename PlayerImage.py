from PIL import Image, ImageFont, ImageDraw
import requests
import os
import io
import time
import argparse

class PlayerImage():
    def __init__(self, tag: str, apiKey: str) -> None:
        self.tag = tag.upper() if tag[0] != '#' else tag[1:].upper()
        self.apiKey = apiKey
        self.clanless = False
        self.legendLeague = False
        self.previousSeason = False
        self.inTop1000 = False
        self.troopsImage = Image.open('./Images/Empty Images/Empty_Troops.png')
        self.profileImage = Image.open('./Images/Empty Images/Empty_Profile.png')
        self.legendImage = Image.open('./Images/Empty Images/Empty_Legend.png')


    def drawText(self, draw: ImageDraw.ImageDraw, font: int, position: tuple, text: str, fontSize: str, shadowOffset=[0, 0], shadow=True, alignment='left', color=(255, 255, 255)) -> None:
        font = ImageFont.truetype(f'./Fonts/{font}', fontSize)
        black = (0, 0, 0)
        
        w, h = draw.textsize(str(text), font)
        if alignment == 'centered': x, y = position[0] - w/2, position[1] - h/2
        elif alignment == 'right': x, y = position[0] - w, position[1] - h
        elif alignment == 'left': x, y = position

        if shadow:
            draw.text([x + shadowOffset[0], y], str(text), black, font) 
            draw.text([x - shadowOffset[0], y], str(text), black, font)
            draw.text([x, y - shadowOffset[0]], str(text), black, font)
            for i in range(shadowOffset[1]):
                draw.text([x, y + i], str(text), black, font)
                draw.text([x + shadowOffset[0], y + i], str(text), black, font)
                draw.text([x - shadowOffset[0], y + i], str(text), black, font)

        draw.text([x, y], str(text), color, font) 


    def getHomeBaseData(self) -> None:   
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.apiKey}'
        }
        roles = {"member": 'Member', "admin": 'Elder', "coLeader": 'Co-leader', "leader": 'Leader',}

        self.data = requests.get(f'https://api.clashofclans.com/v1/players/%23{self.tag}', headers=headers).json()
        self.name = self.data["name"]
        self.townHallLevel = self.data["townHallLevel"]
        self.townHallWeaponLevel = self.data["townHallWeaponLevel"] if "townHallWeaponLevel" in self.data.keys() else 0
        self.troops = self.data["troops"]
        self.spells = self.data["spells"]
        self.heroes = self.data["heroes"]
        self.expLevel = self.data["expLevel"]
        self.trophies = self.data["trophies"]
        self.league = self.data["league"]["name"] if "league" in self.data.keys() else 'Unranked' 
        self.bestThrophies = self.data["bestTrophies"]
        self.warStars = self.data["warStars"]
        self.attackWins = self.data["attackWins"]
        self.defenseWins = self.data["defenseWins"]
        self.donations = self.data["donations"]
        self.donationsReceived = self.data["donationsReceived"]
        if "legendStatistics" in self.data.keys():
            self.legendLeague = True
            legendStats = self.data["legendStatistics"]
            self.legendCups = legendStats["legendTrophies"]
            self.bestSeasonId = legendStats["bestSeason"]["id"]
            self.bestSeasonCups = legendStats["bestSeason"]["trophies"]
            self.bestSeasonRank = legendStats["bestSeason"]["rank"]
            if "previousSeason" in legendStats.keys():
                self.previousSeason = True
                self.previousSeasonId = legendStats["previousSeason"]["id"]
                self.previousSeasonCups = legendStats["previousSeason"]["trophies"]
                self.previousSeasonRank = legendStats["previousSeason"]["rank"]
            else:
                data = requests.get('https://api.clashofclans.com/v1/leagues/29000022/seasons', headers=headers).json()
                self.previousSeasonId = data["items"][-1]["id"]
            if "rank" in legendStats["currentSeason"].keys():
                self.inTop1000 = True
                self.currentRank = legendStats["currentSeason"]["rank"]
        self.labels = []
        [self.labels.append(label["iconUrls"]["small"]) for label in self.data["labels"]]
        if "role" in self.data.keys():
            self.role = roles[self.data["role"]]
            self.clanName = self.data["clan"]["name"]
            self.warPreference = self.data["warPreference"]
        else: 
            self.role = ''
            self.clanless = True            

        if self.bestThrophies >= 5000:
            self.bestRank = 'Legend League'
        elif self.bestThrophies >= 4700:
            self.bestRank = 'Titan League I'
        elif self.bestThrophies >= 4400:
            self.bestRank = 'Titan League II'
        elif self.bestThrophies >= 4100:
            self.bestRank = 'Titan League III'
        elif self.bestThrophies >= 3800:
            self.bestRank = 'Champion League I'    
        elif self.bestThrophies >= 3500:
            self.bestRank = 'Champion League II'
        elif self.bestThrophies >= 3200:
            self.bestRank = 'Champion League III'
        elif self.bestThrophies >= 3000:
            self.bestRank = 'Master League I'
        elif self.bestThrophies >= 2800:
            self.bestRank = 'Master League II'
        elif self.bestThrophies >= 2600:
            self.bestRank = 'Master League III'
        elif self.bestThrophies >= 2400:
            self.bestRank = 'Crystal League I'
        elif self.bestThrophies >= 2200:
            self.bestRank = 'Crystal League II'
        elif self.bestThrophies >= 2000:
            self.bestRank = 'Crystal League III'
        elif self.bestThrophies >= 1800:
            self.bestRank = 'Gold League I'
        elif self.bestThrophies >= 1600:
            self.bestRank = 'Gold League II'
        elif self.bestThrophies >= 1400:
            self.bestRank = 'Gold League III'
        elif self.bestThrophies >= 1200:
            self.bestRank = 'Silver League I'
        elif self.bestThrophies >= 1000:
            self.bestRank = 'Silver League II'
        elif self.bestThrophies >= 800:
            self.bestRank = 'Silver League III'
        elif self.bestThrophies >= 600:
            self.bestRank = 'Bronze League I'
        elif self.bestThrophies >= 500:
            self.bestRank = 'Bronze League II'
        else:
            self.bestRank = 'Bronze League III'

        
    def makeProfileImage(self) -> None:
        # Draw on profile
        draw = ImageDraw.Draw(self.profileImage)

        # Experience level
        self.drawText(draw, 'Supercell-Magic_5.ttf', [57, 71], self.expLevel, 26, [1, 5], alignment='centered')

        # Name
        self.drawText(draw, 'Supercell-Magic_5.ttf', [105, 30], self.name, 26, [1, 5])

        # Tag
        self.drawText(draw, 'CCBackBeat-Light_5.ttf', [105, 64], '#' + self.tag, 24, [1, 5], color=(220, 220, 220))

        # Role
        self.drawText(draw, 'CCBackBeat-Light_5.ttf', [105, 92], self.role, 24, [1, 5])

        # Troops donated
        self.drawText(draw, 'CCBackBeat-Light_5.ttf', [270, 447], self.donations, 22, alignment='centered', shadow=False)

        # Troops received
        self.drawText(draw, 'CCBackBeat-Light_5.ttf', [580, 447], self.donationsReceived, 22, alignment='centered', shadow=False)

        # Attacks won
        self.drawText(draw, 'CCBackBeat-Light_5.ttf', [880, 447], self.attackWins, 22, alignment='centered', shadow=False)

        # Defense won
        self.drawText(draw, 'CCBackBeat-Light_5.ttf', [1230, 447], self.defenseWins, 22, alignment='centered', shadow=False)

        # Warstars
        self.drawText(draw, 'Supercell-Magic_5.ttf', [1040, 341], self.warStars, 25, [1, 5])

        # All time  best league image
        x, y = 940, 214
        allTimeBestImage = Image.open(f'./Images/Profile/Small Leagues/{self.bestRank}.png')
        self.profileImage.paste(allTimeBestImage, (x, y))

        # All time best
        self.drawText(draw, 'Supercell-Magic_5.ttf', [1055, 238], self.bestThrophies, 25, [1, 5])

        # Current throphies
        self.drawText(draw, 'Supercell-Magic_5.ttf', [1076, 119], self.trophies, 30, [1, 6])
        
        # Big league image
        if self.league != 'Unranked':
            x, y = 837, 20
            leagueImage = Image.open(f'./Images/Profile/Big Leagues/{"".join(self.league.split()[:2])}.png')
            self.profileImage.paste(leagueImage, (x, y))

        # Cover attack and defense wins        
        else:
            draw.rectangle([625, 433, 1275, 465], (74, 76, 120))

        # League name
        self.drawText(draw, 'Supercell-Magic_5.ttf', [1020, 75], self.league, 19, [1, 5])

        # Labels
        for label in self.labels:
            data = io.BytesIO(requests.get(label).content)
            icon = Image.open(data).resize((81, 81))
            x, y = int(28 + 96.5 * self.labels.index(label)), 147 # 96.5 because of a 1 pixel differnce between label 2 and 3, int always rounds down to get the correct value
            self.profileImage.paste(icon, (x,y), mask=icon)

        if not self.clanless:
            # Badge
            x, y = 680, 200
            w = h = 225
            data = io.BytesIO(requests.get(self.data["clan"]["badgeUrls"]["medium"]).content)
            self.badge = Image.open(data).resize((w, h))
            self.profileImage.paste(self.badge, (x - int(w/2), y - int(h/2)), mask=self.badge)

            # Name
            self.drawText(draw, 'Supercell-Magic_5.ttf', [680, 50], self.clanName, 22, [1, 4], alignment='centered')

            # War preference
            warPreferenceImage = Image.open(f'./Images/Profile/War Preference/{self.warPreference}.png')
            w, h = warPreferenceImage.size
            x, y = int(680 - w/2), int(355 - h/2)
            self.profileImage.paste(warPreferenceImage, (x, y))
        else:
            x, y = 610, 30
            noClan = Image.open('./Images/Profile/noClan.png')
            self.profileImage.paste(noClan, (x, y))
        
        # Disable current rank since it's not accurate
        #if self.inTop1000:
        #    inTop1000FontSizes = {1: 65, 2: 50, 3: 40}
        #    inTop1000ShadowSize = {1: [4, 12], 2: [2, 8], 3: [2, 8]}
        #    i = len(str(self.currentRank))
        #    self.drawText(draw, 'Supercell-Magic_5.ttf', [930, 105], self.currentRank, inTop1000FontSizes[i], inTop1000ShadowSize[i], alignment='centered', color=(255, 252, 206))
        
    
    def makeTroopImage(self) -> None:
        draw = ImageDraw.Draw(self.troopsImage)
        troopLocation = {"Barbarian": (470, 71), "Archer": (553, 71), "Giant": (636, 71), "Goblin": (719, 71), "Wall Breaker": (802, 71), "Balloon": (887, 71), "Wizard": (970, 71), "Healer": (1053, 71), "Dragon": (1136, 71), "P.E.K.K.A": (470, 156), "Baby Dragon": (553, 156), "Miner": (636, 156), "Electro Dragon": (719, 156), "Yeti": (802, 156), "Dragon Rider": (887, 156), "Minion": (970, 156), "Hog Rider": (1053, 156), "Valkyrie": (1136, 156), "Golem": (470, 242), "Witch": (553, 242), "Lava Hound": (636, 242), "Bowler": (719, 242), "Ice Golem": (802, 242), "Headhunter": (887, 242), "Wall Wrecker": (468, 608), "Battle Blimp": (551, 608), "Stone Slammer": (634, 608), "Siege Barracks": (717, 608), "Log Launcher": (801, 608), "Flame Flinger": (884, 608), "L.A.S.S.I": (33, 535), "Electro Owl": (120, 535), "Mighty Yak": (205, 535), "Unicorn": (290, 535),}
        pets = ["L.A.S.S.I", "Mighty Yak", "Electro Owl", "Unicorn"]
        troops = ["Barbarian", "Archer", "Giant", "Goblin", "Wall Breaker", "Balloon", "Wizard", "Healer", "Dragon", "P.E.K.K.A", "Baby Dragon", "Miner", "Electro Dragon", "Yeti", "Dragon Rider", "Minion", "Hog Rider", "Valkyrie", "Golem", "Witch", "Lava Hound", "Bowler", "Ice Golem", "Headhunter", "Wall Wrecker", "Battle Blimp", "Stone Slammer", "Siege Barracks", "Log Launcher", "Flame Flinger", "L.A.S.S.I", "Electro Owl", "Mighty Yak", "Unicorn",]

        for troop in self.troops:
            troopName = troop["name"]
            if troop["village"] == 'builderBase':
                pass
            else:
                troopLevel = troop["level"]
                troopMaxLevel = troop["maxLevel"]
                if troopName in pets:
                    levelImageOffset = [6 + troopLocation[troopName][0], 45 + troopLocation[troopName][1]]
                    levelImage = Image.open(f'./Images/Troops/Pets/{"maxed" if troopLevel == troopMaxLevel else ""}{troopName}.png')
                    self.troopsImage.paste(levelImage, troopLocation[troopName])
                    if troopLevel != troopMaxLevel: 
                        x, y = levelImageOffset[0] + 10, levelImageOffset[1] + 10 - 3
                        self.drawText(draw, 'CCBackBeat-Light_5.ttf', [x, y], troopLevel, 16, [.75, 4], alignment='centered')
                
                elif troopName in troops:   
                    levelImageOffset = [6 + troopLocation[troopName][0], 45 + troopLocation[troopName][1]]  
                    troopImage = Image.open(f'./Images/Troops/Troops/{troopName}.png')
                    self.troopsImage.paste(troopImage, troopLocation[troopName])
                    if troopLevel >= 2:
                        levelImage = Image.open(f'./Images/Troops/Level Icons/{"nonMaxed" if troopLevel != troopMaxLevel else "maxed"}.png')
                        self.troopsImage.paste(levelImage, levelImageOffset, mask=levelImage)
                        x, y = levelImageOffset[0] + 10, levelImageOffset[1] + 10 - 3
                        self.drawText(draw, 'CCBackBeat-Light_5.ttf', [x, y], troopLevel, 16, [.75, 4], alignment='centered')
        
        # Spells
        spellLocation = {"Lightning Spell": (470, 382), "Healing Spell": (554, 382), "Rage Spell": (636, 382), "Jump Spell": (721, 382), "Freeze Spell": (804, 382), "Clone Spell": (887, 382), "Invisibility Spell": (970, 382), "Poison Spell": (1055, 382), "Earthquake Spell": (1138, 382), "Haste Spell": (470, 466), "Skeleton Spell": (553, 466), "Bat Spell": (636, 466),}
        for spell in self.spells:     
            spellName = spell["name"]
            spellLevel = spell["level"]
            levelImageOffset = [5 + spellLocation[spellName][0], 47 + spellLocation[spellName][1]]
            spellImage = Image.open(f'./Images/Troops/Spells/{spellName}.png')
            self.troopsImage.paste(spellImage, spellLocation[spellName])
            if spellLevel >= 2:
                spellMaxLevel = spell["maxLevel"]
                levelImage = Image.open(f'./Images/Troops/Level Icons/{"nonMaxed" if spellLevel != spellMaxLevel else "maxed"}.png')
                self.troopsImage.paste(levelImage, levelImageOffset, mask=levelImage)
                x, y = levelImageOffset[0] + 10, levelImageOffset[1] + 10 - 3
                self.drawText(draw, 'CCBackBeat-Light_5.ttf', [x, y], spellLevel, 16, [.75, 4], alignment='centered')

        # Heroes
        heroLocation = {"Barbarian King": (33, 387), "Archer Queen": (120, 387), "Grand Warden": (205, 387), "Royal Champion": (290, 387),}
        for hero in self.heroes:
            if hero['village'] == 'builderBase':
                pass
            else:
                heroName = hero["name"]
                heroLevel = hero["level"]
                heroMaxLevel = hero["maxLevel"]
                if heroLevel == heroMaxLevel:
                    heroImage = Image.open(f'./Images/Troops/Heroes/maxed{heroName}.png')
                    self.troopsImage.paste(heroImage, heroLocation[heroName])
                else:
                    levelImageOffset = [6 + heroLocation[heroName][0], 45 + heroLocation[heroName][1]]
                    heroImage = Image.open(f'./Images/Troops/Heroes/{heroName}.png')
                    self.troopsImage.paste(heroImage, heroLocation[heroName])
                    x, y = levelImageOffset[0] + levelImage.size[0]/2, levelImageOffset[1] + levelImage.size[1]/2 - 3
                    self.drawText(draw, 'CCBackBeat-Light_5.ttf', [x, y], heroLevel, 16, [.75, 4], alignment='centered')

        # Townhall image
        townHallImage = Image.open(f'./Images/Troops/TownHalls/{self.townHallLevel}_{self.townHallWeaponLevel}.png')
        self.troopsImage.paste(townHallImage, [0, 12])


    def makeLegendImage(self) -> None:        
        months = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December",}
        bestSeasonFontSize = {1: 50, 2: 40, 3: 29, 4: 23, 5: 20, 6: 16}
        bestSeasonShadowSize = {1: [2, 8], 2: [2, 7], 3: [2, 6], 4: [1, 4], 5: [1, 5], 6: [1, 4]}
        previousSeasonFontSize = {1: 30, 2: 25, 3: 22, 4: 17, 5: 16, 6: 13}
        previousSeasonShadowSize = {1: [2, 8], 2: [2, 6], 3: [1, 5], 4: [1, 4], 5: [1, 4], 6: [1, 4]}
        if self.legendLeague:
            draw = ImageDraw.Draw(self.legendImage)

            # Total legend cups
            self.drawText(draw, 'CCBackBeat-Light_5.ttf', [1042, 45], 'Legend Trophies', 20, [1, 4])
            self.drawText(draw, 'Supercell-Magic_5.ttf', [1250, 115], self.legendCups, 25, [1, 5], alignment='right')

            # Best season
            year, month = self.bestSeasonId.split('-')
            self.drawText(draw, 'CCBackBeat-Light_5.ttf', [125, 45], f'Best: {months[month]} {year} Season', 20, [1, 4])
            self.drawText(draw, 'Supercell-Magic_5.ttf', [285, 122], self.bestSeasonCups, 26, [1, 5], alignment='right')
            self.drawText(draw, 'Supercell-Magic_5.ttf', [70, 87], self.bestSeasonRank, bestSeasonFontSize[len(str(self.bestSeasonRank))], bestSeasonShadowSize[len(str(self.bestSeasonRank))], alignment='centered')
            
            # Previous legend season
            if self.previousSeason:
                self.drawText(draw, 'Supercell-Magic_5.ttf', [685, 98], self.previousSeasonCups, 23, [1, 5])
                self.drawText(draw, 'Supercell-Magic_5.ttf', [590, 103], self.previousSeasonRank, previousSeasonFontSize[len(str(self.previousSeasonRank))], previousSeasonShadowSize[len(str(self.previousSeasonRank))], alignment='centered')
            else:
                didNotPlace = Image.open('./Images/Legend League/did not place.png')
                self.legendImage.paste(didNotPlace, [555, 71])
            year, month = self.previousSeasonId.split('-')
            self.drawText(draw, 'CCBackBeat-Light_5.ttf', [555, 45], f"Previous: {months[month]} {year} Season", 20, [1, 4])
            

    def makeHomeBaseImage(self) -> None:
        self.getHomeBaseData()
        self.makeProfileImage()
        self.makeTroopImage()
        self.makeLegendImage()

        left = Image.open(f'./Images/Empty Images/{"no" if self.clanless else ""}clanLeft.png')
        right = Image.open('./Images/Empty Images/right.png')
        down = Image.open('./Images/Empty Images/Down.png')
        homeVillage = Image.open('./Images/Empty Images/Home Village.png')
        
        try: os.mkdir('Results')
        except FileExistsError: pass
        try: os.mkdir(f'./Results/#{self.tag}')
        except FileExistsError: pass
        
        # Vertically add profile image, troop image and legend image (in case it's needed)
        if self.legendLeague:
            fullProfileImage = [self.profileImage, self.legendImage, self.troopsImage]
        else:
            fullProfileImage = [self.profileImage, self.troopsImage]

        widths, heights = zip(*(i.size for i in fullProfileImage))
        totalWidth = max(widths)
        maxHeight = sum(heights)
        fullHomeBase = Image.new('RGB', (totalWidth, maxHeight))
        yOffset = 0
        for im in fullProfileImage:
            fullHomeBase.paste(im, (0, yOffset))
            yOffset += im.size[1]

        fullHomeBase.show()
        fullHomeBase.save(f'./Results/#{self.tag}/Full Homebase.png')

        # Vertically add to the top
        verticalImages = [homeVillage, fullHomeBase]
        widths, heights = zip(*(i.size for i in verticalImages))
        totalWidth = max(widths)
        maxHeight = sum(heights)
        deviceLikeHomeBase = Image.new('RGB', (totalWidth, maxHeight))
        yOffset = 0
        for im in verticalImages:
            deviceLikeHomeBase.paste(im, (0, yOffset))
            yOffset += im.size[1]

        # Horizontally add the left and right base image
        verticalImage = deviceLikeHomeBase.crop([0, 0, deviceLikeHomeBase.size[0], left.size[1]])
        horizontalImages = [left, verticalImage, right]
        widths, heights = zip(*(i.size for i in horizontalImages))
        totalWidth = sum(widths)
        maxHeight = max(heights)

        deviceLikeHomeBase = Image.new('RGB', (totalWidth, maxHeight))
        xOffset = 0
        for im in horizontalImages:
            deviceLikeHomeBase.paste(im, (xOffset, 0))
            xOffset += im.size[0]

        # Add the bar at the bottom
        deviceLikeHomeBase.paste(down, [left.size[0], left.size[1] - down.size[1]])

        # Draw exp level again in the top left
        draw = ImageDraw.Draw(deviceLikeHomeBase)
        self.drawText(draw, 'Supercell-Magic_5.ttf', [65, 54], self.expLevel, 26, [1, 5], alignment='centered', color=(130,130,130))
        
        deviceLikeHomeBase.save(f'./Results/#{self.tag}/Device Like HomeBase.png')
        deviceLikeHomeBase.show()
        

if __name__ == '__main__':
    apiKey = '' # Fill in your own API key           
    if apiKey == '':
        raise ValueError('Please fill in an API key first. Get one on https://developer.clashofclans.com/.')

    parser = argparse.ArgumentParser(description='This script will make an image of an account profile of Clash of Clans.')
    parser.add_argument('tag', type=str, help='the account tag of the profile.', nargs='?')
    args = parser.parse_args()
    tag = args.tag

    if tag == None:
        tag = str(input('Tag: '))

    start = time.time()
    w = PlayerImage(tag, apiKey)
    w.makeHomeBaseImage()
    print(f'Time elapsed: {round(time.time()- start, 2)}s')
