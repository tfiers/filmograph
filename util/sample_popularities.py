from scraper.themoviedb import get_api_response
from math import log10
from numpy import logspace

# '/tv/popular' or '/movie/popular'
resource = '/tv/popular'
total_pages = get_api_response(resource).get('total_pages')

# Make a number of logaritmically spaced page numbers
pages = logspace(0, log10(total_pages), num=40)

# Make page numbers integer and remove duplicates.
for page in sorted(list(set(map(int, map(round, pages))))):
    response = get_api_response(resource, {'page': page})
    s = 'Page {:>4} - Rank {:>6}: '.format(page, 1+20*(page-1))
    # {name} for tv, {title} for movies
    s += 'id:{id:>7}, pop:{popularity:>11.6f}, title: {name}'.format(
            **response['results'][0])
    print(s)


# # On feb 21, 2016, 14:50:
# 
# Page    1 - Rank      1: id: 293660, pop: 100.588117, title: Deadpool
# Page    2 - Rank     21: id: 337339, pop:  13.263573, title: Fast 8
# Page    3 - Rank     41: id:  99861, pop:  10.428954, title: Avengers: Age of Ultron
# Page    4 - Rank     61: id: 254128, pop:   8.815580, title: San Andreas
# Page    5 - Rank     81: id:    272, pop:   7.448537, title: Batman Begins
# Page    6 - Rank    101: id: 109445, pop:   6.736811, title: Frozen
# Page    7 - Rank    121: id: 228161, pop:   6.211710, title: Home
# Page    8 - Rank    141: id:     98, pop:   5.759105, title: Gladiator
# Page   10 - Rank    181: id:     85, pop:   5.142720, title: Raiders of the Lost Ark
# Page   12 - Rank    221: id: 276907, pop:   4.816447, title: Legend
# Page   14 - Rank    261: id:   2502, pop:   4.478305, title: The Bourne Supremacy
# Page   17 - Rank    321: id:   1995, pop:   4.192859, title: Lara Croft: Tomb Raider
# Page   20 - Rank    381: id: 241239, pop:   3.966789, title: A Most Violent Year
# Page   24 - Rank    461: id:  14756, pop:   3.687617, title: Ip Man
# Page   29 - Rank    561: id:    180, pop:   3.456564, title: Minority Report
# Page   34 - Rank    661: id: 333696, pop:   3.282390, title: Naked Among Wolves
# Page   41 - Rank    801: id:    792, pop:   3.074311, title: Platoon
# Page   49 - Rank    961: id:    588, pop:   2.872516, title: Silent Hill
# Page   58 - Rank   1141: id:  45132, pop:   2.704285, title: Super
# Page   70 - Rank   1381: id: 115782, pop:   2.548534, title: Jobs
# Page   83 - Rank   1641: id:     79, pop:   2.407385, title: Hero
# Page   99 - Rank   1961: id:  45772, pop:   2.272290, title: Gnomeo & Juliet
# Page  118 - Rank   2341: id: 264656, pop:   2.144595, title: The Homesman
# Page  141 - Rank   2801: id: 290595, pop:   2.030838, title: The Huntsman Winter's War
# Page  168 - Rank   3341: id: 381929, pop:   1.913917, title: The Bad Boy of Bowling
# Page  201 - Rank   4001: id:   9401, pop:   1.814912, title: 2 Days in the Valley
# Page  240 - Rank   4781: id:  11880, pop:   1.715823, title: Dog Soldiers
# Page  286 - Rank   5701: id:  10994, pop:   1.624374, title: White Oleander
# Page  342 - Rank   6821: id:   9819, pop:   1.524365, title: Marvin's Room
# Page  408 - Rank   8141: id: 127962, pop:   1.434756, title: Leviathan
# Page  487 - Rank   9721: id: 140456, pop:   1.343100, title: For No Good Reason
# Page  581 - Rank  11601: id:  37531, pop:   1.263502, title: Everyman's War
# Page  693 - Rank  13841: id:  49190, pop:   1.195260, title: Antarctic Journal
# Page  827 - Rank  16521: id:  75657, pop:   1.139082, title: Screwed
# Page  987 - Rank  19721: id:  77399, pop:   1.097500, title: Incense for the Damned
# 
# 
# Some movies I know and their popularities and estimated pages and ranks:
# 
# Page  300 - Rank   6000: id:  83666, pop:   1.554227, title: Moonrise Kingdom
# Page ++++ - Rank  +++++: id: 330697, pop:   0.487665, title: Belgica
# Page+++++ - Rank ++++++: id:  44103, pop:   0.000018, title: "Priest Daens" (original_title: Daens)
# 






# -------- Same for TV ---------------------------------------------------------------
# 
# Page    1 - Rank      1: id:   1622, pop:  40.639585, title: Supernatural
# Page    2 - Rank     21: id:   1416, pop:  12.749498, title: Grey's Anatomy
# Page    3 - Rank     41: id:   1421, pop:   9.565431, title: Modern Family
# Page    4 - Rank     61: id:  50825, pop:   8.032156, title: Sleepy Hollow
# Page    5 - Rank     81: id:  61733, pop:   7.070791, title: Empire
# Page    6 - Rank    101: id:   1100, pop:   6.366545, title: How I Met Your Mother
# Page    7 - Rank    121: id:  62858, pop:   5.958811, title: Colony
# Page    8 - Rank    141: id:   1417, pop:   5.459257, title: Glee
# Page   10 - Rank    181: id:   1855, pop:   4.847509, title: Star Trek: Voyager
# Page   12 - Rank    221: id:  54344, pop:   4.096852, title: The Leftovers
# Page   14 - Rank    261: id:   4656, pop:   3.812327, title: WWE Raw
# Page   17 - Rank    321: id:  49011, pop:   3.339721, title: Mom
# Page   20 - Rank    381: id:  44549, pop:   3.086589, title: Nashville
# Page   24 - Rank    461: id:   2458, pop:   2.806956, title: CSI: NY
# Page   29 - Rank    561: id:   4419, pop:   2.543068, title: Real Time with Bill Maher
# Page   35 - Rank    681: id:  46316, pop:   2.273492, title: Motive
# Page   41 - Rank    801: id:   2430, pop:   2.118562, title: Doc Martin
# Page   49 - Rank    961: id:  10000, pop:   1.942934, title: Twice in a Lifetime
# Page   59 - Rank   1161: id:   4223, pop:   1.794250, title: Cagney & Lacey
# Page   70 - Rank   1381: id:   9240, pop:   1.676819, title: Love & War
# Page   84 - Rank   1661: id:   2661, pop:   1.567546, title: Kamen Rider
# Page  100 - Rank   1981: id:  61499, pop:   1.479784, title: Marry Me
# Page  119 - Rank   2361: id:  24777, pop:   1.397029, title: Flying High
# Page  143 - Rank   2841: id:  12544, pop:   1.341825, title: Street Sharks
# Page  170 - Rank   3381: id:  20345, pop:   1.266164, title: Wan Wan Celeb Soreyuke! Tetsunoshin
# Page  203 - Rank   4041: id:  42370, pop:   1.221258, title: Unsupervised
# Page  242 - Rank   4821: id:  13120, pop:   1.167674, title: Code Monkeys
# Page  289 - Rank   5761: id:  26887, pop:   1.121500, title: Bruce's Guest Night
# Page  346 - Rank   6901: id:   8617, pop:   1.090000, title: RPM
# Page  412 - Rank   8221: id:  42884, pop:   1.053312, title: Snooki & Jwoww
# Page  492 - Rank   9821: id:  13771, pop:   1.027000, title: The Doctors
# Page  588 - Rank  11741: id:  57973, pop:   1.014649, title: Jersey Strong
# Page  702 - Rank  14021: id:  40410, pop:   1.009371, title: Work It
# Page  838 - Rank  16741: id:  53728, pop:   1.006000, title: Mazinkaizer SKL
# Page 1000 - Rank  19981: id:  11031, pop:   1.004186, title: Wish Me Luck
# 
# 
# Some TV shows I know and their popularities, and estimated pages and ranks:
# 
# Page    1 - Rank     10: id:   1399, pop:  21.040038, title: Game of Thrones
# Page   55 - Rank   1000: id:  61920, pop:   1.861354, title: Catastrophe
# Page ++++ - Rank  +++++: id:  29082, pop:   0.744549, title: De Wereld Draait Door
# Page+++++ - Rank ++++++: id:  43181, pop:   0.004904, title: Van Vlees en Bloed
