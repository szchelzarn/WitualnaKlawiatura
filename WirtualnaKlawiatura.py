import cv2
import numpy as np

klawiatura = np.zeros((600, 1000, 3), np.uint8)

ustawienia_klawiszy_1 = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T",
              5: "A", 6: "S", 7: "D", 8: "F", 9: "G",
              10: "Z", 11: "X", 12: "C", 13: "V", 14: "B"}


#licznik
frames = 0
litera_index = 0


def litera(litera_index, tekst, podswietlenie):
        # Klawisze
    if litera_index == 0:
        x = 0
        y = 0
    elif litera_index == 1:
        x = 200
        y = 0
    elif litera_index == 2:
        x = 400
        y = 0
    elif litera_index == 3:
        x = 600
        y = 0
    elif litera_index == 4:
        x = 800
        y = 0
    elif litera_index == 5:
        x = 0
        y = 200
    elif litera_index == 6:
        x = 200
        y = 200
    elif litera_index == 7:
        x = 400
        y = 200
    elif litera_index == 8:
        x = 600
        y = 200
    elif litera_index == 9:
        x = 800
        y = 200
    elif litera_index == 10:
        x = 0
        y = 400
    elif litera_index == 11:
        x = 200
        y = 400
    elif litera_index == 12:
        x = 400
        y = 400
    elif litera_index == 13:
        x = 600
        y = 400
    elif litera_index == 14:
        x = 800
        y = 400

    width = 200
    height = 200
    th = 3 # grubosc
    if podswietlenie is True:
        cv2.rectangle(klawiatura, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
    else:
        cv2.rectangle(klawiatura, (x + th, y + th), (x + width - th, y + height - th), (255, 0, 0), th)
    # Ustawienia tekstu
    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale = 10
    font_th = 4
    text_size = cv2.getTextSize(tekst, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    cv2.putText(klawiatura, tekst, (text_x, text_y), font_letter, font_scale, (255, 0, 0), font_th)

#podswietlenie

for i in range(15):
    if  i == 5:
            light = True
    else:
        light = False
    litera(i, ustawienia_klawiszy_1[i], light)


cv2.imshow("klawiatura", klawiatura)
cv2.waitKey(0)
cv2.destroyAllWindows()