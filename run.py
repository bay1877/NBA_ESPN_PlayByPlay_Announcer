from bs4 import BeautifulSoup
import requests, TTS, time, sys

#todo add fun sounds for threes and such, add params for different modes (verbose, succinct, scores and misses only)

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

def get_play_table(url):
    game = requests.get(url, headers=headers)
    soup = BeautifulSoup(game.text, 'html.parser')
    soup = soup.findAll("div", class_="accordion-content collapse in")[1]
    return soup.findAll('tr')[1:]

def get_team_names(url):
    game = requests.get(url, headers=headers)
    soup = BeautifulSoup(game.text, 'html.parser')
    soup = soup.find("title")
    title_array = soup.text.split(" ")
    team1_name = ""
    team1_abbr = ""
    team2_name = ""
    team2_abbr = ""
    with open("Teams.txt") as file:
        for line in file:
            if title_array[0] in line:
                team1_name = title_array[0]
                team1_abbr = line.split(" ")[0].lower()
            elif title_array[2] in line:
                team2_name = title_array[2]
                team2_abbr = line.split(" ")[0].lower()

    return (team1_name, team1_abbr, team2_name, team2_abbr)

def get_team_name(name_list, team_logo_string):
    # print(team_logo_string)
    if name_list[1] in team_logo_string:
        return name_list[0]
    elif name_list[3] in team_logo_string:
        return name_list[2]
    else:
        print("Team name error")


def compare_times(last_time, maybe_new_time):
    #retrun -1 if after last time, 0 if same as last time, 1 if before (less time on clock), -2 if new quarter
    last_split = last_time.split(":")
    new_split = maybe_new_time.split(":")
    print(last_split, new_split)
    last_seconds_total = 0
    new_seconds_total = 0

    if len(last_split) == 1:
        last_seconds_total = float(last_split[0])
    elif len(last_split) == 2:
        last_seconds_total = float(last_split[0])*60 + float(last_split[1])
    else:
        print("Last split error: ", last_split)

    if len(new_split) == 1:
        new_seconds_total = float(new_split[0])
    elif len(new_split) == 2:
        new_seconds_total = float(new_split[0])*60 + float(new_split[1])
    else:
        print("New split error: ", new_split)

    if len(last_split) < len(new_split):
        # this is a new quarter
        return -2
    else: #same quarter
        if last_seconds_total > new_seconds_total:
            return 1
        elif last_seconds_total < new_seconds_total:
            return -1
        else:
            return 0


def get_zero_time(score_table): #this breaks if there is no zero time
    play = score_table[0]
    time = play.find('td', class_='time-stamp').text
    return str(time)

def get_min_plays(score_table):
    length = len(score_table)
    if length < 15:
        return length
    return 15

def start_and_read(last_time, score_table, name_list):
    print("A play was made at a new time.")
    for i in range(get_min_plays(score_table)-1, -1, -1):
        play = score_table[i]
        time = play.find('td', class_='time-stamp').text
        desc = play.find('td', class_='game-details').text
        score = play.find('td', class_='combined-score').text
        team_logo = play.find('img')['src']
        print(" Zero Time: {} Read Time: {} ".format(last_time, time))
        comparison = compare_times(last_time, time)
        if comparison == 1:
            # print(time, desc, score)
            TTS.read("{} at {}.".format(get_team_name(name_list, team_logo), time))
            # TTS.read(time)
            if "three" in desc and "makes" in desc:
                TTS.playBang()
            elif "dunk" in desc and "makes" in desc:
                TTS.playDunk()
            elif "makes free throw" in desc:
                TTS.playFreethrow()
            TTS.read(desc)
            if ("makes" in desc):
                TTS.read(score)
        elif comparison == -2:
            return -1
    return 0


def new_quarter(url, name_list):
    last_time = "13:00"
    last_count = 0
    while True:
        score_table = get_play_table(url)
        zero_time = get_zero_time(score_table)
        print("Last time: ", last_time, " Last count: ", last_count, " Zero time: ", zero_time)
        if last_time != zero_time:
            if start_and_read(last_time, score_table, name_list) == -1:
                break
            last_time = zero_time  # update lasttime
        # elif count_recent_score(score_table, last_time) > last_count:
        #     last_count = add_and_read(last_time, last_count, score_table)
        else:
            time.sleep(10)


def main():
    if len(sys.argv) != 3:
        print("Usage: run.py <espn play by play url> <quarter #>")
    else:
        url = sys.argv[1]
        quarter_num = int(sys.argv[2])
        name_list = get_team_names(url)
        for i in range(quarter_num, 5):
            new_quarter(url, name_list)

if __name__ == '__main__':
    main()

# get_score_table()