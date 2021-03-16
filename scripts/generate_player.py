
def generate_player(mpd_location, dash_alg):
    print("Generating player.html with mpd: " + mpd_location + " dash alg: " +dash_alg)

    with open('player_template.html') as f:
        contents = f.read()

    contents = contents.replace('<<MPD_LOCATION>>', mpd_location)
    contents = contents.replace('<<DASH_ALG>>', dash_alg)

    with open('player.html', 'w') as f:
        f.write(contents)

    print("Done")

if __name__ == '__main__':
    generate_player('data/mp', 'abrBla')