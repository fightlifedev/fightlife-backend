fans = []

fan_names = [
    "Marcus Lane","Jalen Ross","Tyrese Cole","Kayla Monroe","Andre Bishop",
    "Loren Tate","Jasmine Cruz","Bryce Holloway","Tiana Banks","Corey Sloan",
    "Damien Cross","Zay Parker","Nia Rivers","Makai Bell","Trevor King",
    "Aliyah Stone","Jordan Moss","Isaiah York","Rico Hayes","Cam Vaughn",
    "Miles Carter","Derek Lowe","Noah Steele","Mia Brooks","Trey Wilson",
    "Avery Lane","Kobe Hunter","Darius Ford","Sky Monroe","Jaylin West",
    "Mason Cole","Carter Blake","Dev Green","Sincere Hall","Nova Banks",
    "Roman Hayes","Kali Rivers","Tatum Bell","Ace Sloan","Milo York",
    "Jace Holloway","Kingston Tate","Armani Cruz","Ari Monroe","Chance Cole",
    "Bryson West","Rylan Ford","Legend Brooks","Sage Parker","Dior Stone",
    "Phoenix Bell","Kai Hayes","Reese Lane","Zion King","Aaliyah Moss",
    "Nico Cross","Mila Rivers","Jett Carter","Harlow Sloan","Knox York",
    "Kendall Brooks","Jade Holloway","Ryder Cruz","Maddox Tate","Luca Bell",
    "Ellis Hayes","Blake Monroe","River Lane","Aspen Cole","Dallas King",
    "Hunter Ford","Cash Parker","Sienna Moss","Briar West","Koda Sloan",
    "Oakley Rivers","Bodhi Stone","Atlas Cruz","Zuri Brooks","Halo Bell",
    "Wren Carter","Nash Hayes","Lennox Ford","Storm King","Ember Lane",
    "True Parker","Royal Moss","Onyx Rivers","Zen Monroe","Echo Sloan",
    "Cove Bell","Arrow Tate","Indy Cruz","Quest Brooks","Dream Hayes"
]

favorite_fighters = [
    "Devon Duffee",
    "Malik Brunson",
    "Conor McGregor",
    "Jon Jones",
    "Alex Pereira",
    "Sean O'Malley",
    "Islam Makhachev",
    "Khamzat Chimaev",
    "Israel Adesanya",
    "Gervonta Davis"
]

cities = [
    "Detroit","Las Vegas","Miami","Los Angeles","Houston",
    "Chicago","Atlanta","Phoenix","New York","Baltimore"
]

sports = ["MMA", "Boxing"]

for name in fan_names:
    fans.append({
        "name": name,
        "type": "fan",
        "favorite_sport": sports[len(name) % len(sports)],
        "favorite_fighter": favorite_fighters[len(name) % len(favorite_fighters)],
        "activity_level": (len(name) % 10) + 1,
        "loyalty": ((len(name) * 2) % 10) + 1,
        "toxicity": ((len(name) * 3) % 10) + 1,
        "city": cities[len(name) % len(cities)],

        "social": {
            "handle": "",
            "display_name": name,
            "verified": False,
            "followers": 0,
            "following": 0,
            "posts": [],
            "bio": "Fight fan",
            "activity_level": (len(name) % 10) + 1
        }
    })
