import ast
import curses
import os
import time
import random
from subprocess import Popen, PIPE

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import textwrap

def main(stdscr):
    def print_haiku(haiku, title):
        stdscr.clear()
        text = '\n'.join([' '.join(line) for line in haiku])
        stdscr.addstr(title + '\n')
        stdscr.addstr('-'*30 + '\n')
        stdscr.addstr(text)
        stdscr.refresh()
        time.sleep(random.random()/10)

    def write_haiku(words, title):
        haiku = [[],[],[]]
        i = 0

        for word in words:
            if word == 'i++':
                i += 1
            elif word == 'i--':
                i -= 1
            elif word[0] == '-':
                while (len(haiku[i][-1]) > 0):
                    haiku[i][-1] = haiku[i][-1][:-1]
                    print_haiku(haiku, title)
                haiku[i].pop()
            else:
                haiku[i].append('')
                for c in word:
                    haiku[i][-1] += c
                    print_haiku(haiku, title)

        return haiku

    def generate_image(haiku,
                       MAX_W=696, MAX_H=200,
                       background_color=(255, 255, 255, 0),
                       foreground_color=(0,0,0),
                       pad=10, title_pad=20, line_pad=50
                       ):

        im = Image.new('RGB', (MAX_W, MAX_H), background_color)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype("arial.ttf", 30)

        # Center the text vertically
        total_h = sum([
            draw.textsize(line, font=font)[1] + pad for line in haiku
        ]) + (title_pad - pad)
        current_h = (MAX_H - total_h)/2

        # Write the title
        title = haiku[0]
        w,h = draw.textsize(title, font=font)
        draw.text(
            ((MAX_W - w) / 2, current_h), title,
            font=font, fill=foreground_color
        )
        current_h += h + title_pad

        # Put a line between the title and the haiku
        draw.line([(line_pad, current_h-title_pad/2), (MAX_W - line_pad, current_h-title_pad/2)], fill=(0,0,0))

        # Write the haiku
        for line in haiku[1:]:
            w, h = draw.textsize(line, font=font)
            draw.text(((MAX_W - w) / 2, current_h), line, font=font, fill=foreground_color)
            current_h += h + pad

        im.save('haiku.png')

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    df = pd.read_csv('haikus.csv')

    while True:
        for i,row in df.sample(frac=1).iterrows():
            words = ast.literal_eval((row['path']))
            haiku = write_haiku(words, row['title'])
            haiku = [' '.join(line) for line in haiku]

            generate_image([row['title']] + haiku)
            proc = Popen(
                'brother_ql_create -s 62 -m QL-800 haiku.png > haiku.bin',
                shell=True
            )
            proc.wait()
            proc = Popen('lp -d ql-800 haiku.bin', shell=True, stdout=PIPE, stderr=PIPE)
            proc.wait()

            time.sleep(2)
            stdscr.addstr("\n\nPlease press the button\nto generate another\nNYC haiku.")
            stdscr.refresh()
            #stdscr.getkey()

            while True:
                if GPIO.input(18) == False:
                    break


curses.wrapper(main)
