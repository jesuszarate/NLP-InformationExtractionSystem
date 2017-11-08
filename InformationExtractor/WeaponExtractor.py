from InformationExtractor import IO as io

stories = io.readAllFiles()


def formatStory(story, weaponSet):
    items = story.split('\n')

    for item in items:
        s = item.split(':')
        if len(s) > 1:
            s[0] = s[0].replace(" ", "")
            weapons = s[1].split('/')
            if s[0] == 'Weapon':
                for weapon in weapons:
                    weapon = weapon.strip()
                    if weapon != '-':
                        weaponSet.add(weapon)
    return weaponSet

weaponSet = set()
for story in stories:
    s = formatStory(story, weaponSet)

io.writeWeapons(weaponSet)