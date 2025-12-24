import json
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'world_data.json')

# Rich Data Dictionary (Top 50 + VIPs)
# Included: Existing 21 (Preserved) + ~30 Top Tourists
# Images: Unsplash (High Quality) or Wikimedia (Specific)
RICH_DATA = {
    # --- EXISTING VIPs (Preserved) ---
    "IL": {"name": "Israel", "slug": "israel", "network": "Pelephone", "capital": "Jerusalem", "landmark": "the Western Wall", "plug": "Type H", "intro": "High-speed coverage in Tel Aviv, Jerusalem and the North.", "image_url": "https://plus.unsplash.com/premium_photo-1697729976900-1089e894f05b?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NDQzOTA3fA&ixlib=rb-4.1.0", "is_popular": True},
    "US": {"name": "USA", "slug": "usa", "network": "T-Mobile", "capital": "Washington D.C.", "landmark": "Times Square", "plug": "Type A/B", "intro": "Travel across the United States with high-speed data.", "image_url": "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=1600&q=80", "is_popular": True},
    "JP": {"name": "Japan", "slug": "japan", "network": "Docomo", "capital": "Tokyo", "landmark": "Shibuya Crossing", "plug": "Type A", "intro": "Stay connected in Tokyo, Kyoto, and beyond.", "image_url": "https://images.unsplash.com/photo-1542051841857-5f90071e7989?w=1600&q=80", "is_popular": True},
    "FR": {"name": "France", "slug": "france", "network": "Orange", "capital": "Paris", "landmark": "the Eiffel Tower", "plug": "Type E", "intro": "Enjoy Paris and the French Riviera without roaming fees.", "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1600&q=80", "is_popular": True},
    "TH": {"name": "Thailand", "slug": "thailand", "network": "AIS", "capital": "Bangkok", "landmark": "the Grand Palace", "plug": "Type A/B", "intro": "Island hopping and Bangkok city life with reliable internet.", "image_url": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=1600&q=80", "is_popular": True},
    "GB": {"name": "United Kingdom", "slug": "united-kingdom", "network": "EE", "capital": "London", "landmark": "Big Ben", "plug": "Type G", "intro": "London, Scotland, and Wales coverage.", "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1600&q=80", "is_popular": True},
    "IT": {"name": "Italy", "slug": "italy", "network": "TIM", "capital": "Rome", "landmark": "the Colosseum", "plug": "Type L", "intro": "Pizza, pasta, and instant connectivity in Rome.", "image_url": "https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=1600&q=80", "is_popular": True},
    "ES": {"name": "Spain", "slug": "spain", "network": "Movistar", "capital": "Madrid", "landmark": "Sagrada Família", "plug": "Type F", "intro": "Barcelona, Madrid, and sunny beaches.", "image_url": "https://images.unsplash.com/photo-1543783207-ec64e4d95325?w=1600&q=80", "is_popular": True},
    "DE": {"name": "Germany", "slug": "germany", "network": "Telekom", "capital": "Berlin", "landmark": "Brandenburg Gate", "plug": "Type F", "intro": "Experience Munich, Berlin, and the Autobahn connected.", "image_url": "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=1600&q=80", "is_popular": True},
    "TR": {"name": "Turkey", "slug": "turkey", "network": "Turkcell", "capital": "Ankara", "landmark": "Hagia Sophia", "plug": "Type F", "intro": "From Istanbul to Cappadocia, stay online.", "image_url": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1600&q=80", "is_popular": True},
    "AU": {"name": "Australia", "slug": "australia", "network": "Telstra", "capital": "Canberra", "landmark": "Sydney Opera House", "plug": "Type I", "intro": "Outback adventures and city vibes in Sydney.", "image_url": "https://images.unsplash.com/photo-1523482580638-01c63b6dd919?w=1600&q=80", "is_popular": True},
    "KR": {"name": "South Korea", "slug": "south-korea", "network": "SK Telecom", "capital": "Seoul", "landmark": "Gyeongbokgung Palace", "plug": "Type F", "intro": "High-tech connectivity in Seoul.", "image_url": "https://images.unsplash.com/photo-1538485399081-7191377e8241?w=1600&q=80", "is_popular": True},
    "SG": {"name": "Singapore", "slug": "singapore", "network": "Singtel", "capital": "Singapore", "landmark": "Marina Bay Sands", "plug": "Type G", "intro": "Seamless 5G in the Lion City.", "image_url": "https://images.unsplash.com/photo-1565967511849-76a60a516170?w=1600&q=80", "is_popular": True},
    "ID": {"name": "Indonesia", "slug": "indonesia", "network": "Telkomsel", "capital": "Jakarta", "landmark": "Bali Beaches", "plug": "Type C", "intro": "Surf, relax, and stream in Bali.", "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=1600&q=80", "is_popular": True},
    "CA": {"name": "Canada", "slug": "canada", "network": "Rogers", "capital": "Ottawa", "landmark": "Niagara Falls", "plug": "Type A", "intro": "From the Rockies to Toronto, stay covered.", "image_url": "https://images.unsplash.com/photo-1503614472-8c93d56e92ce?w=1600&q=80", "is_popular": True},
    "MX": {"name": "Mexico", "slug": "mexico", "network": "Telcel", "capital": "Mexico City", "landmark": "Chichen Itza", "plug": "Type A", "intro": "Tacos, beaches, and 4G data.", "image_url": "https://images.unsplash.com/photo-1512813195386-6cf811ad3542?w=1600&q=80", "is_popular": True},
    "GR": {"name": "Greece", "slug": "greece", "network": "Cosmote", "capital": "Athens", "landmark": "the Acropolis", "plug": "Type F", "intro": "Island vibes and ancient history.", "image_url": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=1600&q=80", "is_popular": True},
    "PT": {"name": "Portugal", "slug": "portugal", "network": "MEO", "capital": "Lisbon", "landmark": "Belem Tower", "plug": "Type F", "intro": "Explore Lisbon and Algarve online.", "image_url": "https://images.unsplash.com/photo-1569959220744-ff553533f492?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NTI3OTA2fA&ixlib=rb-4.1.0", "is_popular": True},
    "NL": {"name": "Netherlands", "slug": "netherlands", "network": "KPN", "capital": "Amsterdam", "landmark": "the Canals", "plug": "Type C/F", "intro": "Cycling and connectivity in Amsterdam.", "image_url": "https://images.unsplash.com/photo-1547750341-26482cf3a2ac?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NTI3OTMxfA&ixlib=rb-4.1.0", "is_popular": True},
    "CH": {"name": "Switzerland", "slug": "switzerland", "network": "Swisscom", "capital": "Bern", "landmark": "The Matterhorn", "plug": "Type J", "intro": "Alps, chocolate, and fast internet.", "image_url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=1600&q=80", "is_popular": True},
    "AE": {"name": "UAE", "slug": "united-arab-emirates", "network": "Etisalat", "capital": "Abu Dhabi", "landmark": "Burj Khalifa", "plug": "Type G", "intro": "Luxury travel with luxury speed.", "image_url": "https://plus.unsplash.com/premium_photo-1661919068698-40e7b78f196a?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NDQwNTg0fA&ixlib=rb-4.1.0", "is_popular": True},

    # --- NEW TIER A (Enriched) ---
    "VN": {"name": "Vietnam", "slug": "vietnam", "network": "Viettel", "capital": "Hanoi", "landmark": "Ha Long Bay", "plug": "Type A/C", "intro": "Pho, coffee, and 4G everywhere.", "image_url": "https://images.unsplash.com/photo-1528127269322-539801943592?w=1600&q=80"},
    "MY": {"name": "Malaysia", "slug": "malaysia", "network": "Maxis", "capital": "Kuala Lumpur", "landmark": "Petronas Towers", "plug": "Type G", "intro": "Diverse culture and digital connectivity.", "image_url": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=1600&q=80"},
    "PH": {"name": "Philippines", "slug": "philippines", "network": "Globe", "capital": "Manila", "landmark": "Palawan", "plug": "Type A", "intro": "7,000 islands, one reliable connection.", "image_url": "https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=1600&q=80"},
    "IN": {"name": "India", "slug": "india", "network": "Jio", "capital": "New Delhi", "landmark": "Taj Mahal", "plug": "Type D", "intro": "Incredible India, instantly connected.", "image_url": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=1600&q=80"},
    "CN": {"name": "China", "slug": "china", "network": "China Mobile", "capital": "Beijing", "landmark": "Great Wall", "plug": "Type A", "intro": "Stay connected behind the Great Wall.", "image_url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=1600&q=80"},
    "BR": {"name": "Brazil", "slug": "brazil", "network": "Vivo", "capital": "Brasilia", "landmark": "Christ the Redeemer", "plug": "Type N", "intro": "Samba, carnival, and seamless data.", "image_url": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=1600&q=80"},
    "AR": {"name": "Argentina", "slug": "argentina", "network": "Personal", "capital": "Buenos Aires", "landmark": "Patagonia", "plug": "Type I", "intro": "Tango and trekking with full bars.", "image_url": "https://images.unsplash.com/photo-1589909202802-8f4aadce1849?w=1600&q=80"},
    "ZA": {"name": "South Africa", "slug": "south-africa", "network": "Vodacom", "capital": "Pretoria", "landmark": "Table Mountain", "plug": "Type M", "intro": "Safari streaming and Cape Town views.", "image_url": "https://images.unsplash.com/photo-1580060839134-75a5edca2e27?w=1600&q=80"},
    "EG": {"name": "Egypt", "slug": "egypt", "network": "Vodafone", "capital": "Cairo", "landmark": "Pyramids of Giza", "plug": "Type C", "intro": "Ancient history, modern connection.", "image_url": "https://images.unsplash.com/photo-1539768942893-daf53e448371?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NDQzNDc5fA&ixlib=rb-4.1.0"},
    "MA": {"name": "Morocco", "slug": "morocco", "network": "Maroc Telecom", "capital": "Rabat", "landmark": "Sahara Desert", "plug": "Type C", "intro": "Souks and deserts without offline maps.", "image_url": "https://images.unsplash.com/photo-1539020140153-e479b8c22e70?w=1600&q=80"},
    "CZ": {"name": "Czech Republic", "slug": "czech-republic", "network": "O2", "capital": "Prague", "landmark": "Charles Bridge", "plug": "Type E", "intro": "Bohemian vibes and fast 4G.", "image_url": "https://images.unsplash.com/photo-1541849546-216549ae216d?w=1600&q=80"},
    "HU": {"name": "Hungary", "slug": "hungary", "network": "Telekom", "capital": "Budapest", "landmark": "Parliament Building", "plug": "Type C", "intro": "Budapest nights and reliable data.", "image_url": "https://images.unsplash.com/photo-1516764681174-2e86fa26c278?w=1600&q=80"},
    "PL": {"name": "Poland", "slug": "poland", "network": "Orange", "capital": "Warsaw", "landmark": "Old Town Market Place", "plug": "Type E", "intro": "History and modernity connected.", "image_url": "https://images.unsplash.com/photo-1519197924294-4ba991a11128?w=1600&q=80"},
    "IE": {"name": "Ireland", "slug": "ireland", "network": "Vodafone", "capital": "Dublin", "landmark": "Cliffs of Moher", "plug": "Type G", "intro": "Emerald Isle adventures online.", "image_url": "https://images.unsplash.com/photo-1590089415225-401cd6f9ad43?w=1600&q=80"},
    "SE": {"name": "Sweden", "slug": "sweden", "network": "Telia", "capital": "Stockholm", "landmark": "Gamla Stan", "plug": "Type F", "intro": "Scandi-style connectivity.", "image_url": "https://images.unsplash.com/photo-1509356843151-3e7d96241e11?w=1600&q=80"},
    "NO": {"name": "Norway", "slug": "norway", "network": "Telenor", "capital": "Oslo", "landmark": "Fjords", "plug": "Type F", "intro": "Fjords and fast internet.", "image_url": "https://images.unsplash.com/photo-1520630098670-fd4050961c02?w=1600&q=80"},
    "DK": {"name": "Denmark", "slug": "denmark", "network": "TDC", "capital": "Copenhagen", "landmark": "Nyhavn", "plug": "Type K", "intro": "Hygge and high-speed data.", "image_url": "https://images.unsplash.com/photo-1513622470522-26c3c8a854bc?w=1600&q=80"},
    "FI": {"name": "Finland", "slug": "finland", "network": "Elisa", "capital": "Helsinki", "landmark": "Northern Lights", "plug": "Type F", "intro": "Land of a thousand lakes and 5G.", "image_url": "https://images.unsplash.com/photo-1535928392-48dfcd37ebae?w=1600&q=80"},
    "IS": {"name": "Iceland", "slug": "iceland", "network": "Siminn", "capital": "Reykjavik", "landmark": "Blue Lagoon", "plug": "Type F", "intro": "Fire, ice, and full bars.", "image_url": "https://images.unsplash.com/photo-1476610182048-b716b8518aae?w=1600&q=80"},
    "AT": {"name": "Austria", "slug": "austria", "network": "A1", "capital": "Vienna", "landmark": "Schönbrunn Palace", "plug": "Type F", "intro": "Classical music and modern tech.", "image_url": "https://images.unsplash.com/photo-1516550893923-42d28e5677af?w=1600&q=80"},
    "BE": {"name": "Belgium", "slug": "belgium", "network": "Proximus", "capital": "Brussels", "landmark": "Grand Place", "plug": "Type E", "intro": "Waffles, beer, and bandwidth.", "image_url": "https://plus.unsplash.com/premium_photo-1661963734315-be9904fe0a07?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NTI3OTU5fA&ixlib=rb-4.1.0"},
    "NZ": {"name": "New Zealand", "slug": "new-zealand", "network": "Spark", "capital": "Wellington", "landmark": "Milford Sound", "plug": "Type I", "intro": "Middle Earth coverage.", "image_url": "https://images.unsplash.com/photo-1507699622177-388898d9903d?w=1600&q=80"},
    "HR": {"name": "Croatia", "slug": "croatia", "network": "HT", "capital": "Zagreb", "landmark": "Dubrovnik Walls", "plug": "Type F", "intro": "Adriatic coast connectivity.", "image_url": "https://images.unsplash.com/photo-1555992828-ca4dbe41d294?w=1600&q=80"},
    "CL": {"name": "Chile", "slug": "chile", "network": "Entel", "capital": "Santiago", "landmark": "Torres del Paine", "plug": "Type L", "intro": "From Andes to ocean, stay online.", "image_url": "https://images.unsplash.com/photo-1478827387698-1527781a4887?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NDQ0MDc0fA&ixlib=rb-4.1.0"},
    "CO": {"name": "Colombia", "slug": "colombia", "network": "Claro", "capital": "Bogota", "landmark": "Cartagena Old Town", "plug": "Type A", "intro": "Coffee and connection.", "image_url": "https://images.unsplash.com/photo-1531761535209-180857e963b9?w=1600&q=80"},
    "PE": {"name": "Peru", "slug": "peru", "network": "Movistar", "capital": "Lima", "landmark": "Machu Picchu", "plug": "Type A", "intro": "Inca trails and internet trails.", "image_url": "https://images.unsplash.com/photo-1526392060635-9d6019884377?w=1600&q=80"},
    "QA": {"name": "Qatar", "slug": "qatar", "network": "Ooredoo", "capital": "Doha", "landmark": "Souq Waqif", "plug": "Type G", "intro": "Desert luxury and 5G.", "image_url": "https://images.unsplash.com/photo-1575379583168-3e4b341f530e?w=1600&q=80"},
    "SA": {"name": "Saudi Arabia", "slug": "saudi-arabia", "network": "STC", "capital": "Riyadh", "landmark": "Kingdom Centre", "plug": "Type G", "intro": "Kingdom-wide coverage.", "image_url": "https://images.unsplash.com/photo-1586724237569-f3d0c1dee8c6?w=1600&q=80"},
    "MD": {"name": "Moldova", "slug": "moldova", "network": "Orange", "capital": "Chisinau", "landmark": "Orheiul Vechi", "plug": "Type F", "intro": "Wine country connectivity.", "image_url": "https://images.unsplash.com/photo-1629045951387-6d86eb2aad3d?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NDQ0MTU5fA&ixlib=rb-4.1.0"},

    'CI': {
        'name': "Cote d'Ivoire",
        'slug': "cote-divoire",
        'code': "CI",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Yamoussoukro",
        'landmark': "Basilica of Our Lady of Peace",
        'plug': "Universal",
        'intro': "Stay connected in Cote d'Ivoire with high-speed data.",
        'image_url': "static/countries/cote-divoire.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1601221656510-e23d747fec7c?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'AE': {
        'name': "United Arab Emirates",
        'slug': "united-arab-emirates",
        'code': "AE",
        'region': "Asia",
        'network': "Best Local Network",
        'capital': "Abu Dhabi",
        'landmark': "Burj Khalifa",
        'plug': "Universal",
        'intro': "Stay connected in United Arab Emirates with high-speed data.",
        'image_url': "static/countries/united-arab-emirates.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/United,Arab,Emirates,landscape/all"
    },
    'MM': {
        'name': "Myanmar",
        'slug': "myanmar",
        'code': "MM",
        'region': "Asia",
        'network': "Best Local Network",
        'capital': "Naypyidaw",
        'landmark': "Shwedagon Pagoda",
        'plug': "Universal",
        'intro': "Stay connected in Myanmar with high-speed data.",
        'image_url': "static/countries/myanmar.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Myanmar,landscape/all"
    },
    'AI': {
        'name': "Anguilla",
        'slug': "anguilla",
        'code': "AI",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "The Valley",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Anguilla with high-speed data.",
        'image_url': "static/countries/anguilla.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Anguilla,landscape/all"
    },
    'AG': {
        'name': "Antigua and Barbuda",
        'slug': "antigua-and-barbuda",
        'code': "AG",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Saint John's",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Antigua and Barbuda with high-speed data.",
        'image_url': "static/countries/antigua-and-barbuda.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Antigua,and,Barbuda,landscape/all"
    },
    'AW': {
        'name': "Aruba",
        'slug': "aruba",
        'code': "AW",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Oranjestad",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Aruba with high-speed data.",
        'image_url': "static/countries/aruba.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Aruba,landscape/all"
    },
    'BS': {
        'name': "Bahamas",
        'slug': "bahamas",
        'code': "BS",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Nassau",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Bahamas with high-speed data.",
        'image_url': "static/countries/bahamas.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Bahamas,landscape/all"
    },
    'BH': {
        'name': "Bahrain",
        'slug': "bahrain",
        'code': "BH",
        'region': "Asia",
        'network': "Best Local Network",
        'capital': "Manama",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Bahrain with high-speed data.",
        'image_url': "static/countries/bahrain.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1548755212-2b46ee259868?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'BJ': {
        'name': "Benin",
        'slug': "benin",
        'code': "BJ",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Porto-Novo",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Benin with high-speed data.",
        'image_url': "static/countries/benin.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Benin,landscape/all"
    },
    'BM': {
        'name': "Bermuda",
        'slug': "bermuda",
        'code': "BM",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Hamilton",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Bermuda with high-speed data.",
        'image_url': "static/countries/bermuda.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Bermuda,landscape/all"
    },
    'BT': {
        'name': "Bhutan",
        'slug': "bhutan",
        'code': "BT",
        'region': "Asia",
        'network': "Best Local Network",
        'capital': "Thimphu",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Bhutan with high-speed data.",
        'image_url': "static/countries/bhutan.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Bhutan,landscape/all"
    },
    'BQ': {
        'name': "Bonaire",
        'slug': "bonaire",
        'code': "BQ",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Kralendijk",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Bonaire with high-speed data.",
        'image_url': "static/countries/bonaire.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Bonaire,landscape/all"
    },
    'BW': {
        'name': "Botswana",
        'slug': "botswana",
        'code': "BW",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Gaborone",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Botswana with high-speed data.",
        'image_url': "static/countries/botswana.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Botswana,landscape/all"
    },
    'BN': {
        'name': "Brunei",
        'slug': "brunei",
        'code': "BN",
        'region': "Asia",
        'network': "Best Local Network",
        'capital': "Bandar Seri Begawan",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Brunei with high-speed data.",
        'image_url': "static/countries/brunei.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Brunei,landscape/all"
    },
    'BF': {
        'name': "Burkina Faso",
        'slug': "burkina-faso",
        'code': "BF",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Ouagadougou",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Burkina Faso with high-speed data.",
        'image_url': "static/countries/burkina-faso.jpg",
        'is_popular': False,
        'image_source_url': "https://plus.unsplash.com/premium_photo-1699699368327-a1887e5a6ce6?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'CM': {
        'name': "Cameroon",
        'slug': "cameroon",
        'code': "CM",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Yaoundé",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Cameroon with high-speed data.",
        'image_url': "static/countries/cameroon.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1637244018403-785e7fa8707a?q=80&w=1243&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'CV': {
        'name': "Cape Verde",
        'slug': "cape-verde",
        'code': "CV",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Praia",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Cape Verde with high-speed data.",
        'image_url': "static/countries/cape-verde.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Cape,Verde,landscape/all"
    },
    'KY': {
        'name': "Cayman Islands",
        'slug': "cayman-islands",
        'code': "KY",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "George Town",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Cayman Islands with high-speed data.",
        'image_url': "static/countries/cayman-islands.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Cayman,Islands,landscape/all"
    },
    'CF': {
        'name': "Central African Republic",
        'slug': "central-african-republic",
        'code': "CF",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Bangui",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Central African Republic with high-speed data.",
        'image_url': "static/countries/central-african-republic.jpg",
        'is_popular': False,
        'image_source_url': "https://plus.unsplash.com/premium_photo-1661832611972-b6ee1aba3581?q=80&w=1975&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'TD': {
        'name': "Chad",
        'slug': "chad",
        'code': "TD",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "N'Djamena",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Chad with high-speed data.",
        'image_url': "static/countries/chad.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Chad,landscape/all"
    },
    'CW': {
        'name': "Curacao",
        'slug': "curacao",
        'code': "CW",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Willemstad",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Curacao with high-speed data.",
        'image_url': "static/countries/curacao.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Curacao,landscape/all"
    },
    'DM': {
        'name': "Dominica",
        'slug': "dominica",
        'code': "DM",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Roseau",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Dominica with high-speed data.",
        'image_url': "static/countries/dominica.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Dominica,landscape/all"
    },
    'CD': {
        'name': "DR Congo",
        'slug': "dr-congo",
        'code': "CD",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Kinshasa",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in DR Congo with high-speed data.",
        'image_url': "static/countries/dr-congo.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/DR,Congo,landscape/all"
    },
    'CG': {
        'name': "Republic of the Congo",
        'slug': "republic-of-the-congo",
        'code': "CG",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Brazzaville",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Republic of the Congo with high-speed data.",
        'image_url': "static/countries/republic-of-the-congo.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1671665306335-2fe71e9b7128?q=80&w=1332&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'SZ': {
        'name': "Eswatini",
        'slug': "eswatini",
        'code': "SZ",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Mbabane",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Eswatini with high-speed data.",
        'image_url': "static/countries/eswatini.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Eswatini,landscape/all"
    },
    'ET': {
        'name': "Ethiopia",
        'slug': "ethiopia",
        'code': "ET",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Addis Ababa",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Ethiopia with high-speed data.",
        'image_url': "static/countries/ethiopia.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1572888195250-3037a59d3578?q=80&w=1200&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'FO': {
        'name': "Faroe Islands",
        'slug': "faroe-islands",
        'code': "FO",
        'region': "Europe",
        'network': "Best Local Network",
        'capital': "Tórshavn",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Faroe Islands with high-speed data.",
        'image_url': "static/countries/faroe-islands.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Faroe,Islands,landscape/all"
    },
    'FJ': {
        'name': "Fiji",
        'slug': "fiji",
        'code': "FJ",
        'region': "Oceania",
        'network': "Best Local Network",
        'capital': "Suva",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Fiji with high-speed data.",
        'image_url': "static/countries/fiji.jpg",
        'is_popular': False,
        'image_source_url': "https://plus.unsplash.com/premium_photo-1716025288906-6b6f44f882cb?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'GF': {
        'name': "French Guiana",
        'slug': "french-guiana",
        'code': "GF",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Cayenne",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in French Guiana with high-speed data.",
        'image_url': "static/countries/french-guiana.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/French,Guiana,landscape/all"
    },
    'GA': {
        'name': "Gabon",
        'slug': "gabon",
        'code': "GA",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Libreville",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Gabon with high-speed data.",
        'image_url': "static/countries/gabon.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Gabon,landscape/all"
    },
    'GM': {
        'name': "Gambia",
        'slug': "gambia",
        'code': "GM",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Banjul",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Gambia with high-speed data.",
        'image_url': "static/countries/gambia.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1448099940878-e0c48ea3a165?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'GI': {
        'name': "Gibraltar",
        'slug': "gibraltar",
        'code': "GI",
        'region': "Europe",
        'network': "Best Local Network",
        'capital': "Gibraltar",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Gibraltar with high-speed data.",
        'image_url': "static/countries/gibraltar.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Gibraltar,landscape/all"
    },
    'GL': {
        'name': "Greenland",
        'slug': "greenland",
        'code': "GL",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Nuuk",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Greenland with high-speed data.",
        'image_url': "static/countries/greenland.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Greenland,landscape/all"
    },
    'GD': {
        'name': "Grenada",
        'slug': "grenada",
        'code': "GD",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Saint George's",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Grenada with high-speed data.",
        'image_url': "static/countries/grenada.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1616464654572-43996d6b0133?q=80&w=1333&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'GP': {
        'name': "Guadeloupe",
        'slug': "guadeloupe",
        'code': "GP",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Basse-Terre",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Guadeloupe with high-speed data.",
        'image_url': "static/countries/guadeloupe.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Guadeloupe,landscape/all"
    },
    'GU': {
        'name': "Guam",
        'slug': "guam",
        'code': "GU",
        'region': "Oceania",
        'network': "Best Local Network",
        'capital': "Hagåtña",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Guam with high-speed data.",
        'image_url': "static/countries/guam.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1662863256389-3d897324bd7a?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'GN': {
        'name': "Guinea",
        'slug': "guinea",
        'code': "GN",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Conakry",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Guinea with high-speed data.",
        'image_url': "static/countries/guinea.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1676405956449-64d51e0cc7bf?q=80&w=1073&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'GW': {
        'name': "Guinea-Bissau",
        'slug': "guinea-bissau",
        'code': "GW",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Bissau",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Guinea-Bissau with high-speed data.",
        'image_url': "static/countries/guinea-bissau.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Guinea-Bissau,landscape/all"
    },
    'GY': {
        'name': "Guyana",
        'slug': "guyana",
        'code': "GY",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Georgetown",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Guyana with high-speed data.",
        'image_url': "static/countries/guyana.jpg",
        'is_popular': False,
        'image_source_url': "https://plus.unsplash.com/premium_photo-1712736395839-997c8c9dbd06?q=80&w=1175&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'HT': {
        'name': "Haiti",
        'slug': "haiti",
        'code': "HT",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Port-au-Prince",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Haiti with high-speed data.",
        'image_url': "static/countries/haiti.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1580741186862-c5d0bf2aff33?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'IQ': {
        'name': "Iraq",
        'slug': "iraq",
        'code': "IQ",
        'region': "Asia",
        'network': "Best Local Network",
        'capital': "Baghdad",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Iraq with high-speed data.",
        'image_url': "static/countries/iraq.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1608925086961-dbcd276a0e71?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'IM': {
        'name': "Isle of Man",
        'slug': "isle-of-man",
        'code': "IM",
        'region': "Europe",
        'network': "Best Local Network",
        'capital': "Douglas",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Isle of Man with high-speed data.",
        'image_url': "static/countries/isle-of-man.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1578417525709-5574524d09e2?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'JE': {
        'name': "Jersey",
        'slug': "jersey",
        'code': "JE",
        'region': "Europe",
        'network': "Best Local Network",
        'capital': "Saint Helier",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Jersey with high-speed data.",
        'image_url': "static/countries/jersey.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Jersey,landscape/all"
    },
    'XK': {
        'name': "Kosovo",
        'slug': "kosovo",
        'code': "XK",
        'region': "Europe",
        'network': "Best Local Network",
        'capital': "Pristina",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Kosovo with high-speed data.",
        'image_url': "static/countries/kosovo.jpg",
        'is_popular': False,
        'image_source_url': "https://plus.unsplash.com/premium_photo-1669047983472-1eeb3a5ea6a5?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'LS': {
        'name': "Lesotho",
        'slug': "lesotho",
        'code': "LS",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Maseru",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Lesotho with high-speed data.",
        'image_url': "static/countries/lesotho.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1575285272587-a2523237d6b6?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'LR': {
        'name': "Liberia",
        'slug': "liberia",
        'code': "LR",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Monrovia",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Liberia with high-speed data.",
        'image_url': "static/countries/liberia.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Liberia,landscape/all"
    },
    'LI': {
        'name': "Liechtenstein",
        'slug': "liechtenstein",
        'code': "LI",
        'region': "Europe",
        'network': "Best Local Network",
        'capital': "Vaduz",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Liechtenstein with high-speed data.",
        'image_url': "static/countries/liechtenstein.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Liechtenstein,landscape/all"
    },
    'MO': {
        'name': "Macau",
        'slug': "macau",
        'code': "MO",
        'region': "Asia",
        'network': "Best Local Network",
        'capital': "Macau",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Macau with high-speed data.",
        'image_url': "static/countries/macau.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Macau,landscape/all"
    },
    'MG': {
        'name': "Madagascar",
        'slug': "madagascar",
        'code': "MG",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Antananarivo",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Madagascar with high-speed data.",
        'image_url': "static/countries/madagascar.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1558694440-03ade9215d7b?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'MW': {
        'name': "Malawi",
        'slug': "malawi",
        'code': "MW",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Lilongwe",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Malawi with high-speed data.",
        'image_url': "static/countries/malawi.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1543116696-9e33bf8c3425?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'MV': {
        'name': "Maldives",
        'slug': "maldives",
        'code': "MV",
        'region': "Asia",
        'network': "Best Local Network",
        'capital': "Malé",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Maldives with high-speed data.",
        'image_url': "static/countries/maldives.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Maldives,landscape/all"
    },
    'ML': {
        'name': "Mali",
        'slug': "mali",
        'code': "ML",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Bamako",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Mali with high-speed data.",
        'image_url': "static/countries/mali.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Mali,landscape/all"
    },
    'MQ': {
        'name': "Martinique",
        'slug': "martinique",
        'code': "MQ",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Fort-de-France",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Martinique with high-speed data.",
        'image_url': "static/countries/martinique.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Martinique,landscape/all"
    },
    'MU': {
        'name': "Mauritius",
        'slug': "mauritius",
        'code': "MU",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Port Louis",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Mauritius with high-speed data.",
        'image_url': "static/countries/mauritius.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Mauritius,landscape/all"
    },
    'YT': {
        'name': "Mayotte",
        'slug': "mayotte",
        'code': "YT",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Mamoudzou",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Mayotte with high-speed data.",
        'image_url': "static/countries/mayotte.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1614079757769-6341eb57838d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'MN': {
        'name': "Mongolia",
        'slug': "mongolia",
        'code': "MN",
        'region': "Asia",
        'network': "Best Local Network",
        'capital': "Ulaanbaatar",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Mongolia with high-speed data.",
        'image_url': "static/countries/mongolia.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Mongolia,landscape/all"
    },
    'MS': {
        'name': "Montserrat",
        'slug': "montserrat",
        'code': "MS",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Plymouth",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Montserrat with high-speed data.",
        'image_url': "static/countries/montserrat.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Montserrat,landscape/all"
    },
    'MZ': {
        'name': "Mozambique",
        'slug': "mozambique",
        'code': "MZ",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Maputo",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Mozambique with high-speed data.",
        'image_url': "static/countries/mozambique.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Mozambique,landscape/all"
    },
    'NA': {
        'name': "Namibia",
        'slug': "namibia",
        'code': "NA",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Windhoek",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Namibia with high-speed data.",
        'image_url': "static/countries/namibia.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1649306739639-1ad8ed83978d?q=80&w=1880&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'NR': {
        'name': "Nauru",
        'slug': "nauru",
        'code': "NR",
        'region': "Oceania",
        'network': "Best Local Network",
        'capital': "Yaren",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Nauru with high-speed data.",
        'image_url': "static/countries/nauru.jpg",
        'is_popular': False,
        'image_source_url': "https://plus.unsplash.com/premium_photo-1673240159015-e0ced88df98c?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'NE': {
        'name': "Niger",
        'slug': "niger",
        'code': "NE",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Niamey",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Niger with high-speed data.",
        'image_url': "static/countries/niger.jpg",
        'is_popular': False,
        'image_source_url': "https://plus.unsplash.com/premium_photo-1699536873907-9e9ff18868e3?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'CY': {
        'name': "Northern Cyprus",
        'slug': "northern-cyprus",
        'code': "CY",
        'region': "Europe",
        'network': "Best Local Network",
        'capital': "Nicosia",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Northern Cyprus with high-speed data.",
        'image_url': "static/countries/northern-cyprus.jpg",
        'is_popular': False,
        'image_source_url': "https://plus.unsplash.com/premium_photo-1661957387235-3bc814072fb3?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'PG': {
        'name': "Papua New Guinea",
        'slug': "papua-new-guinea",
        'code': "PG",
        'region': "Oceania",
        'network': "Best Local Network",
        'capital': "Port Moresby",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Papua New Guinea with high-speed data.",
        'image_url': "static/countries/papua-new-guinea.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1615608178738-37d47d27c13d?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'RE': {
        'name': "Reunion",
        'slug': "reunion",
        'code': "RE",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Saint-Denis",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Reunion with high-speed data.",
        'image_url': "static/countries/reunion.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1585697386654-e025feaa654a?q=80&w=1202&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'RW': {
        'name': "Rwanda",
        'slug': "rwanda",
        'code': "RW",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Kigali",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Rwanda with high-speed data.",
        'image_url': "static/countries/rwanda.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1511283878565-0833bf39de9d?q=80&w=1174&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'BL': {
        'name': "Saint Barthelemy",
        'slug': "saint-barthelemy",
        'code': "BL",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Gustavia",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Saint Barthelemy with high-speed data.",
        'image_url': "static/countries/saint-barthelemy.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Saint,Barthelemy,landscape/all"
    },
    'KN': {
        'name': "Saint Kitts and Nevis",
        'slug': "saint-kitts-and-nevis",
        'code': "KN",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Basseterre",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Saint Kitts and Nevis with high-speed data.",
        'image_url': "static/countries/saint-kitts-and-nevis.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Saint,Kitts,and,Nevis,landscape/all"
    },
    'LC': {
        'name': "Saint Lucia",
        'slug': "saint-lucia",
        'code': "LC",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Castries",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Saint Lucia with high-speed data.",
        'image_url': "static/countries/saint-lucia.jpg",
        'is_popular': False,
        'image_source_url': "https://plus.unsplash.com/premium_photo-1661962432490-6188a6420a81?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'MF': {
        'name': "Saint Martin",
        'slug': "saint-martin",
        'code': "MF",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Marigot",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Saint Martin with high-speed data.",
        'image_url': "static/countries/saint-martin.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Saint,Martin,landscape/all"
    },
    'VC': {
        'name': "Saint Vincent and the Grenadines",
        'slug': "saint-vincent-and-the-grenadines",
        'code': "VC",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Kingstown",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Saint Vincent and the Grenadines with high-speed data.",
        'image_url': "static/countries/saint-vincent-and-the-grenadines.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Saint,Vincent,and,the,Grenadines,landscape/all"
    },
    'WS': {
        'name': "Samoa",
        'slug': "samoa",
        'code': "WS",
        'region': "Oceania",
        'network': "Best Local Network",
        'capital': "Apia",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Samoa with high-speed data.",
        'image_url': "static/countries/samoa.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Samoa,landscape/all"
    },
    'SN': {
        'name': "Senegal",
        'slug': "senegal",
        'code': "SN",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Dakar",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Senegal with high-speed data.",
        'image_url': "static/countries/senegal.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1644772088209-c71d5c59f719?q=80&w=1167&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'SC': {
        'name': "Seychelles",
        'slug': "seychelles",
        'code': "SC",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Victoria",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Seychelles with high-speed data.",
        'image_url': "static/countries/seychelles.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Seychelles,landscape/all"
    },
    'SL': {
        'name': "Sierra Leone",
        'slug': "sierra-leone",
        'code': "SL",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Freetown",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Sierra Leone with high-speed data.",
        'image_url': "static/countries/sierra-leone.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Sierra,Leone,landscape/all"
    },
    'BQ': {
        'name': "Sint Eustatius",
        'slug': "sint-eustatius",
        'code': "BQ",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Oranjestad",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Sint Eustatius with high-speed data.",
        'image_url': "static/countries/sint-eustatius.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Sint,Eustatius,landscape/all"
    },
    'SR': {
        'name': "Suriname",
        'slug': "suriname",
        'code': "SR",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Paramaribo",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Suriname with high-speed data.",
        'image_url': "static/countries/suriname.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Suriname,landscape/all"
    },
    'TJ': {
        'name': "Tajikistan",
        'slug': "tajikistan",
        'code': "TJ",
        'region': "Asia",
        'network': "Best Local Network",
        'capital': "Dushanbe",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Tajikistan with high-speed data.",
        'image_url': "static/countries/tajikistan.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Tajikistan,landscape/all"
    },
    'TL': {
        'name': "Timor-Leste",
        'slug': "timor-leste",
        'code': "TL",
        'region': "Asia",
        'network': "Best Local Network",
        'capital': "Dili",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Timor-Leste with high-speed data.",
        'image_url': "static/countries/timor-leste.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1591325408953-ef9298125f96?q=80&w=1176&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'TG': {
        'name': "Togo",
        'slug': "togo",
        'code': "TG",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Lomé",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Togo with high-speed data.",
        'image_url': "static/countries/togo.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1580470846411-b0e734c5ffd6?q=80&w=1172&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'TO': {
        'name': "Tonga",
        'slug': "tonga",
        'code': "TO",
        'region': "Oceania",
        'network': "Best Local Network",
        'capital': "Nuku'alofa",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Tonga with high-speed data.",
        'image_url': "static/countries/tonga.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Tonga,landscape/all"
    },
    'TT': {
        'name': "Trinidad and Tobago",
        'slug': "trinidad-and-tobago",
        'code': "TT",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Port of Spain",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Trinidad and Tobago with high-speed data.",
        'image_url': "static/countries/trinidad-and-tobago.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Trinidad,and,Tobago,landscape/all"
    },
    'TC': {
        'name': "Turks and Caicos Islands",
        'slug': "turks-and-caicos-islands",
        'code': "TC",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Cockburn Town",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Turks and Caicos Islands with high-speed data.",
        'image_url': "static/countries/turks-and-caicos-islands.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Turks,and,Caicos,Islands,landscape/all"
    },
    'UG': {
        'name': "Uganda",
        'slug': "uganda",
        'code': "UG",
        'region': "Africa",
        'network': "Best Local Network",
        'capital': "Kampala",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Uganda with high-speed data.",
        'image_url': "static/countries/uganda.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1537706388178-55c10865b82e?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'VU': {
        'name': "Vanuatu",
        'slug': "vanuatu",
        'code': "VU",
        'region': "Oceania",
        'network': "Best Local Network",
        'capital': "Port Vila",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Vanuatu with high-speed data.",
        'image_url': "static/countries/vanuatu.jpg",
        'is_popular': False,
        'image_source_url': "https://images.unsplash.com/photo-1602587557684-11163fe60c87?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0"
    },
    'VA': {
        'name': "Vatican City",
        'slug': "vatican-city",
        'code': "VA",
        'region': "Europe",
        'network': "Best Local Network",
        'capital': "Vatican City",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in Vatican City with high-speed data.",
        'image_url': "static/countries/vatican-city.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/Vatican,City,landscape/all"
    },
    'VI': {
        'name': "US Virgin Islands",
        'slug': "us-virgin-islands",
        'code': "VI",
        'region': "Americas",
        'network': "Best Local Network",
        'capital': "Charlotte Amalie",
        'landmark': "City Center",
        'plug': "Universal",
        'intro': "Stay connected in US Virgin Islands with high-speed data.",
        'image_url': "static/countries/us-virgin-islands.jpg",
        'is_popular': False,
        'image_source_url': "https://loremflickr.com/800/600/US,Virgin,Islands,landscape/all"
    },
}

# --- SMART GENERATOR FOR THE REST ---
# We will use pycountry or a hardcoded list of standard ISO codes to fill the gaps.
# Since we don't have pycountry, I'll include a minimal ISO map of common countries.
# If a country is not in RICH_DATA, we generate:
# Image: Based on Region
# Intro: Generic Template

REGION_IMAGES = {
    'Europe': "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Neuschwanstein_castle.jpg/800px-Neuschwanstein_castle.jpg",
    'Asia': "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/The_Great_Wall_of_China_at_Jinshanling-edit.jpg/800px-The_Great_Wall_of_China_at_Jinshanling-edit.jpg",
    'Oceania': "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Sydney_Opera_House_-_Dec_2008.jpg/800px-Sydney_Opera_House_-_Dec_2008.jpg",
    'Americas': "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Machu_Picchu_-_Vista_Geral.jpg/800px-Machu_Picchu_-_Vista_Geral.jpg", # Machu Picchu covers general americas travel vibe well
    'Africa': "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Mount_Kilimanjaro_Dec_2009.jpg/800px-Mount_Kilimanjaro_Dec_2009.jpg",
    'Other': "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Grand_Canyon_view_from_Pima_Point_2010.jpg/800px-Grand_Canyon_view_from_Pima_Point_2010.jpg"
}

# Overrides for broken/missing images
MANUAL_IMAGES = {
    'AE': 'https://loremflickr.com/800/600/dubai,skyline',
    'ZA': 'https://loremflickr.com/800/600/cape-town,table-mountain',
    'PT': 'https://loremflickr.com/800/600/lisbon,portugal',
    'IE': 'https://loremflickr.com/800/600/ireland,cliffs',
    'NO': 'https://loremflickr.com/800/600/norway,fjord',
    'IL': 'https://loremflickr.com/800/600/tel-aviv,beach', 
    'NL': 'https://loremflickr.com/800/600/amsterdam,canal',
    'HU': 'https://loremflickr.com/800/600/budapest,parliament',
    'AT': 'https://loremflickr.com/800/600/hallstatt,austria',
    'BE': 'https://loremflickr.com/800/600/bruges,belgium',
    'NZ': 'https://loremflickr.com/800/600/milford-sound,new-zealand',
    'QA': 'https://loremflickr.com/800/600/doha,qatar',
    'CL': 'https://loremflickr.com/800/600/chile,torres-del-paine',
    'EG': 'https://loremflickr.com/800/600/egypt,pyramids',
    'PL': 'https://loremflickr.com/800/600/krakow,poland',
    'SE': 'https://loremflickr.com/800/600/stockholm,sweden',
    'FI': 'https://loremflickr.com/800/600/finland,helsinki',
    'CH': 'https://loremflickr.com/800/600/switzerland,alps',
    'CR': 'https://loremflickr.com/800/600/costa-rica,nature',
    'DO': 'https://loremflickr.com/800/600/dominican-republic,beach',
    'UY': 'https://loremflickr.com/800/600/uruguay,montevideo',
    'HR': 'https://loremflickr.com/800/600/croatia,dubrovnik',
    'JM': 'https://loremflickr.com/800/600/jamaica,beach',
    'AU': 'https://loremflickr.com/800/600/sydney,opera-house',
}

# A larger list of ISO codes to ensure we catch most feed items
# This is a sample; in production we'd want all 249.
# I've included a mix of common missing ones.
EXTRA_ISO_CODES = {
    "AL": "Albania", "AD": "Andorra", "AM": "Armenia", "AZ": "Azerbaijan", "BD": "Bangladesh", "BB": "Barbados", 
    "BY": "Belarus", "BZ": "Belize", "BO": "Bolivia", "BA": "Bosnia and Herzegovina", "BG": "Bulgaria", "KH": "Cambodia", 
    "CR": "Costa Rica", "CI": "Cote d'Ivoire", "CY": "Cyprus", "DO": "Dominican Republic", "EC": "Ecuador", "SV": "El Salvador", 
    "EE": "Estonia", "GE": "Georgia", "GH": "Ghana", "GT": "Guatemala", "HN": "Honduras", "HK": "Hong Kong", "JM": "Jamaica", 
    "JO": "Jordan", "KZ": "Kazakhstan", "KE": "Kenya", "KW": "Kuwait", "KG": "Kyrgyzstan", "LA": "Laos", "LV": "Latvia", 
    "LB": "Lebanon", "LT": "Lithuania", "LU": "Luxembourg", "MO": "Macau", "MK": "North Macedonia", "MT": "Malta", 
    "ME": "Montenegro", "MM": "Myanmar", "NP": "Nepal", "NI": "Nicaragua", "NG": "Nigeria", "OM": "Oman", "PK": "Pakistan", 
    "PA": "Panama", "PY": "Paraguay", "RO": "Romania", "RU": "russia", "RS": "Serbia", "SK": "Slovakia", "SI": "Slovenia", 
    "LK": "Sri Lanka", "TW": "Taiwan", "TZ": "Tanzania", "TN": "Tunisia", "UA": "Ukraine", "UY": "Uruguay", "UZ": "Uzbekistan", 
    "VE": "Venezuela", "ZM": "Zambia", "ZW": "Zimbabwe"
}



UNSPLASH_GAP_FILL = {
    'Albania': 'https://loremflickr.com/800/600/Albania,landscape/all',
    'Andorra': 'https://loremflickr.com/800/600/Andorra,landscape/all',
    'Armenia': 'https://loremflickr.com/800/600/Armenia,landscape/all',
    'Azerbaijan': 'https://loremflickr.com/800/600/Azerbaijan,landscape/all',
    'Bangladesh': 'https://loremflickr.com/800/600/Bangladesh,landscape/all',
    'Barbados': 'https://loremflickr.com/800/600/Barbados,landscape/all',
    'Belarus': 'https://loremflickr.com/800/600/Belarus,landscape/all',
    'Belize': 'https://loremflickr.com/800/600/Belize,landscape/all',
    'Bolivia': 'https://loremflickr.com/800/600/Bolivia,landscape/all',
    'Bosnia and Herzegovina': 'https://loremflickr.com/800/600/Bosnia,landscape/all',
    'Bulgaria': 'https://images.unsplash.com/photo-1633210181101-774c588bc997?q=80&w=1277&auto=format&fit=crop&ixlib=rb-4.1.0',
    'Cambodia': 'https://plus.unsplash.com/premium_photo-1661963188432-5de8a11f21a7?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0',
    'Costa Rica': 'https://loremflickr.com/800/600/Costa,Rica,landscape/all',
    'Cyprus': 'https://loremflickr.com/800/600/Cyprus,landscape/all',
    'Dominican Republic': 'https://loremflickr.com/800/600/Dominican,Republic,landscape/all',
    'Ecuador': 'https://loremflickr.com/800/600/Ecuador,landscape/all',
    'El Salvador': 'https://loremflickr.com/800/600/El,Salvador,landscape/all',
    'Estonia': 'https://plus.unsplash.com/premium_photo-1675716183492-4861033fd024?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8RXN0b25pYSUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0MjczMDJ8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Georgia': 'https://plus.unsplash.com/premium_photo-1673620885239-014f318356f1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8R2VvcmdpYSUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0MjczMDZ8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Ghana': 'https://plus.unsplash.com/premium_photo-1689606828522-86105ce51268?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8R2hhbmElMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3MzA5fDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Guatemala': 'https://images.unsplash.com/photo-1704647250784-f264a682af6b?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NTI4MTQ3fA&ixlib=rb-4.1.0',
    'Honduras': 'https://plus.unsplash.com/premium_photo-1673240159015-e0ced88df98c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8SG9uZHVyYXMlMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3MzE4fDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Hong Kong': 'https://plus.unsplash.com/premium_photo-1661887292499-cbaefdb169ce?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8SG9uZyUyMEtvbmclMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3MzIxfDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Jamaica': 'https://plus.unsplash.com/premium_photo-1677734490428-c11dfb3f1499?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8SmFtYWljYSUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0MjczMjR8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Jordan': 'https://images.unsplash.com/photo-1548786811-dd6e453ccca7?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NTI4MTc2fA&ixlib=rb-4.1.0',
    'Kazakhstan': 'https://images.unsplash.com/photo-1666975823342-3b755b3784d4?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NTI4MjEwfA&ixlib=rb-4.1.0',
    'Kenya': 'https://plus.unsplash.com/premium_photo-1661962383838-89c5659f7762?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8S2VueWElMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3MzM1fDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Kuwait': 'https://images.unsplash.com/photo-1626346073066-f2b7c5bfaefb?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NDQ0MzY3fA&ixlib=rb-4.1.0',
    'Kyrgyzstan': 'https://plus.unsplash.com/premium_photo-1677396179718-fcc01da1b405?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8S3lyZ3l6c3RhbiUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0MjczNDJ8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Laos': 'https://plus.unsplash.com/premium_photo-1661962821338-c07da63995f9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8TGFvcyUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0MjczNDZ8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Latvia': 'https://plus.unsplash.com/premium_photo-1691954120258-4aa92e92732c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8TGF0dmlhJTIwbGFuZHNjYXBlfGVufDB8fHx8MTc2NjQyNzM0OXww&ixlib=rb-4.1.0&q=80&w=1080',
    'Lebanon': 'https://plus.unsplash.com/premium_photo-1697730165870-5d8d3244ffed?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8TGViYW5vbiUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0MjczNTN8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Lithuania': 'https://plus.unsplash.com/premium_photo-1666533242295-82d6df2aab1a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8TGl0aHVhbmlhJTIwbGFuZHNjYXBlfGVufDB8fHx8MTc2NjQyNzM1N3ww&ixlib=rb-4.1.0&q=80&w=1080',
    'Luxembourg': 'https://plus.unsplash.com/premium_photo-1715954843264-18eb40eb4eca?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8THV4ZW1ib3VyZyUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0MjczNjF8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Macau': 'https://images.unsplash.com/photo-1733919505005-d71d8f0272ad?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8TWFjYXUlMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3MzY0fDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Malta': 'https://plus.unsplash.com/premium_photo-1675806357539-32a9cdc34737?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8TWFsdGElMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3MzY4fDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Montenegro': 'https://plus.unsplash.com/premium_photo-1676231364646-3e01fcb0492c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8TW9udGVuZWdybyUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0MjczNzJ8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Myanmar': 'https://plus.unsplash.com/premium_photo-1694475528747-0fa268e4c91f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8TXlhbm1hciUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0MjczNzV8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Nepal': 'https://plus.unsplash.com/premium_photo-1661963741928-673ed7f7c00b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8TmVwYWwlMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3Mzc5fDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Nicaragua': 'https://images.unsplash.com/photo-1494444753080-e0d457fa3563?mark=https%3A%2F%2Fimages.unsplash.com%2Fopengraph%2Flogo.png&mark-w=64&mark-align=top%2Cleft&mark-pad=50&h=630&w=1200&crop=faces%2Cedges&blend-w=1&blend=000000&blend-mode=normal&blend-alpha=10&auto=format&fit=crop&q=60&ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzY2NDQ0NDE4fA&ixlib=rb-4.1.0',
    'Nigeria': 'https://plus.unsplash.com/premium_photo-1726729392828-be2af49e504a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8TmlnZXJpYSUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0MjczODZ8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'North Macedonia': 'https://plus.unsplash.com/premium_photo-1734430860030-b31ed39afbb3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8Tm9ydGglMjBNYWNlZG9uaWElMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3MzkwfDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Oman': 'https://plus.unsplash.com/premium_photo-1688141871984-ce166591b6f8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8T21hbiUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0MjczOTN8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Pakistan': 'https://plus.unsplash.com/premium_photo-1661962344178-19930ba15492?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8UGFraXN0YW4lMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3Mzk3fDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Panama': 'https://plus.unsplash.com/premium_photo-1712736395839-997c8c9dbd06?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8UGFuYW1hJTIwbGFuZHNjYXBlfGVufDB8fHx8MTc2NjQyNzQwMXww&ixlib=rb-4.1.0&q=80&w=1080',
    'Paraguay': 'https://plus.unsplash.com/premium_photo-1670998953029-5022e8eb8d9e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8UGFyYWd1YXklMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3NDA1fDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Romania': 'https://plus.unsplash.com/premium_photo-1729633414521-7cdeb6109aa1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8Um9tYW5pYSUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0Mjc0MDd8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Serbia': 'https://plus.unsplash.com/premium_photo-1661849201240-a0d3bdea40d8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8U2VyYmlhJTIwbGFuZHNjYXBlfGVufDB8fHx8MTc2NjQyNzQxMXww&ixlib=rb-4.1.0&q=80&w=1080',
    'Slovakia': 'https://plus.unsplash.com/premium_photo-1673302607031-c9d8ba2e150e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8U2xvdmFraWElMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3NDE0fDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Slovenia': 'https://plus.unsplash.com/premium_photo-1721060224780-8c8ff9d7d4c7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8U2xvdmVuaWElMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3NDE4fDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Sri Lanka': 'https://plus.unsplash.com/premium_photo-1730145749791-28fc538d7203?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8U3JpJTIwTGFua2ElMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3NDIxfDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Taiwan': 'https://plus.unsplash.com/premium_photo-1661955975506-04d3812be312?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8VGFpd2FuJTIwbGFuZHNjYXBlfGVufDB8fHx8MTc2NjQyNzQyNHww&ixlib=rb-4.1.0&q=80&w=1080',
    'Tanzania': 'https://plus.unsplash.com/premium_photo-1664803534733-ec2cee267e21?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8VGFuemFuaWElMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3NDI4fDA&ixlib=rb-4.1.0&q=80&w=1080',
    'Tunisia': 'https://plus.unsplash.com/premium_photo-1699535657684-bc02eee856e1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8VHVuaXNpYSUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0Mjc0MzJ8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Ukraine': 'https://plus.unsplash.com/premium_photo-1697809003390-ec69e6e3c666?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8VWtyYWluZSUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0Mjc0MzV8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Uruguay': 'https://plus.unsplash.com/premium_photo-1696531220493-bb3be96be9c1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8VXJ1Z3VheSUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0Mjc0Mzh8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Uzbekistan': 'https://plus.unsplash.com/premium_photo-1701158100073-372e621880cb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8VXpiZWtpc3RhbiUyMGxhbmRzY2FwZXxlbnwwfHx8fDE3NjY0Mjc0NDF8MA&ixlib=rb-4.1.0&q=80&w=1080',
    'Venezuela': 'https://plus.unsplash.com/premium_photo-1733317237246-5000d61196b6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8VmVuZXp1ZWxhJTIwbGFuZHNjYXBlfGVufDB8fHx8MTc2NjQyNzQ0NXww&ixlib=rb-4.1.0&q=80&w=1080',
    'Zambia': 'https://plus.unsplash.com/premium_photo-1664302757048-31604d5e9e21?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8WmFtYmlhJTIwbGFuZHNjYXBlfGVufDB8fHx8MTc2NjQyNzQ0OXww&ixlib=rb-4.1.0&q=80&w=1080',
    'Zimbabwe': 'https://plus.unsplash.com/premium_photo-1664302678675-4b0d646cf315?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8WmltYmFid2UlMjBsYW5kc2NhcGV8ZW58MHx8fHwxNzY2NDI3NDUyfDA&ixlib=rb-4.1.0&q=80&w=1080',
    'russia': 'https://plus.unsplash.com/premium_photo-1672062932260-913903b5cf43?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMjA3fDB8MXxzZWFyY2h8MXx8cnVzc2lhJTIwbGFuZHNjYXBlfGVufDB8fHx8MTc2NjQyNzQ1NXww&ixlib=rb-4.1.0&q=80&w=1080',
}

def get_region(country_code):
    # Minimal region mapper for defaults
    code = country_code.upper()
    europe = ['AL', 'AD', 'AT', 'BY', 'BE', 'BA', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'LV', 'LI', 'LT', 'LU', 'MT', 'MD', 'MC', 'ME', 'NL', 'MK', 'NO', 'PL', 'PT', 'RO', 'RU', 'SM', 'RS', 'SK', 'SI', 'ES', 'SE', 'CH', 'TR', 'UA', 'GB', 'VA']
    asia = ['AF', 'AM', 'AZ', 'BH', 'BD', 'BT', 'BN', 'KH', 'CN', 'GE', 'HK', 'IN', 'ID', 'IR', 'IQ', 'IL', 'JP', 'JO', 'KZ', 'KW', 'KG', 'LA', 'LB', 'MO', 'MY', 'MV', 'MN', 'MM', 'NP', 'KP', 'OM', 'PK', 'PS', 'PH', 'QA', 'SA', 'SG', 'KR', 'LK', 'SY', 'TW', 'TJ', 'TH', 'TL', 'TR', 'TM', 'AE', 'UZ', 'VN', 'YE']
    americas = ['US', 'CA', 'MX', 'BR', 'AR', 'CO', 'PE', 'CL', 'CR', 'CU', 'DO', 'EC', 'SV', 'GT', 'HT', 'HN', 'JM', 'NI', 'PA', 'PY', 'UY', 'VE', 'BO', 'BZ']
    africa = ['ZA', 'EG', 'MA', 'NG', 'KE', 'TZ', 'GH', 'CI', 'ZW', 'ZM']
    oceania = ['AU', 'NZ', 'FJ']

    if code in europe: return 'Europe'
    if code in asia: return 'Asia'
    if code in americas: return 'Americas'
    if code in africa: return 'Africa'
    if code in oceania: return 'Oceania'
    return 'Other'


def generate_db():
    world_data = {}
    
    # 1. Add Rich Data
    for code, data in RICH_DATA.items():
        # Preserve source URL
        data['image_source_url'] = data.get('image_url', '')
        
        # Use local static image path for frontend
        if 'slug' in data:
            slug = data['slug']
        else:
            slug = data['name'].lower().replace(" ", "-")
        
        data['image_url'] = f"static/countries/{slug}.jpg"
        
        # Ensure region exists
        if 'region' not in data:
             data['region'] = get_region(code)
        
        # Add code to data
        data['code'] = code
             
        world_data[code] = data
        
    # 2. Add Extra Codes with Defaults
    for code, name in EXTRA_ISO_CODES.items():
        if code in world_data: continue
        
        region = get_region(code)
        slug = name.lower().replace(" ", "-")
        
        # Priority 1: Unsplash Gap Fill (New Scraped Data)
        if name in UNSPLASH_GAP_FILL:
            source_url = UNSPLASH_GAP_FILL[name]
        # Priority 2: Manual Overrides
        elif code in MANUAL_IMAGES:
            source_url = MANUAL_IMAGES[code]
        # Priority 3: Region Fallback (Lowest)
        else:
             source_url = REGION_IMAGES.get(region, REGION_IMAGES['Other'])
            
        world_data[code] = {
            "name": name,
            "slug": slug,
            "code": code,
            "network": "Best Local Network",
            "capital": name, # Fallback
            "landmark": "City Center", # Fallback
            "plug": "Universal", # Fallback
            "intro": f"Stay connected in {name} with high-speed data.",
            "image_source_url": source_url,
            "image_url": f"static/countries/{slug}.jpg",
            "region": region
        }
        
    # Save to world_data.json (Dict format for generate.py)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(world_data, f, indent=2)
        
    # Convert to List for countries.json (for download_images.py & others)
    output_list = list(world_data.values())
        
    # Save to countries.json
    target_file = os.path.join(PROJECT_ROOT, 'data', 'countries.json')
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(output_list, f, indent=2)
    
    print(f"Generated data/countries.json with {len(output_list)} entries.")

if __name__ == "__main__":
    generate_db()
