#Projekt ZPI
"""
Zespołowe przedsięwzięcie inżynierskie  

Autorzy:
Adam Szczepański
Patryk Matusik
Adrian Święs

kierunek: Informatyka Stosowana 
"""
import cv2
import numpy as np
import dlib
import pyglet
import time
from math import hypot
from tkinter import *
import webbrowser

okno = Tk()


#Ładowanie dźwięków
dzwiek = pyglet.media.load("dzwiek.wav", streaming=False)
lewo_dzwiek = pyglet.media.load("lewo.wav", streaming=False)
prawo_dzwiek = pyglet.media.load("prawo.wav", streaming=False)

#Wczytwanie ustawień kamery
cap = cv2.VideoCapture(0)
frame_width = 1280
frame_height = 720
fps = 30.0

tablica = np.zeros((100, 1400), np.uint8) 
tablica [:] = 255

#Punkty orientacyjne twarzy
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("68_punktow_orientacyjnych_twarzy.dat")


#Ustawienia klawiatury
klawiatura = np.zeros((600, 1210, 3), np.uint8)
ustawienie_klawiszy_1 = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T",
              5: ".", 6: "A", 7: "S", 8: "D", 9: "F", 10: "G",
              11: "BACK", 12: "Z", 13: "X", 14: "C", 15: "V", 16: "B", 17: "COPY"}
ustawienie_klawiszy_2 ={0: "Y", 1: "U", 2: "I", 3: "O", 4: "P",
              5: ".", 6: "H", 7: "J", 8: "K", 9: "L", 10: "?", 11:"BACK",
              12: "V", 13: "B", 14: "N", 15: "M", 16: "_", 17: "COPY"}

def litera(litera_index, tekst, podswietlenie):
#Klawisze
    if litera_index == 0:
        x = 0
        y = 0
        font_scale = 10
    elif litera_index == 1:
        x = 200
        y = 0
        font_scale = 10
    elif litera_index == 2:
        x = 400
        y = 0
        font_scale = 10
    elif litera_index == 3:
        x = 600
        y = 0
        font_scale = 10
    elif litera_index == 4:
        x = 800
        y = 0
        font_scale = 10
    elif litera_index == 5:
        x = 1010
        y = 0  
        font_scale = 4
    elif litera_index == 6:
        x = 0
        y = 200
        font_scale = 10
    elif litera_index == 7:
        x = 200
        y = 200
        font_scale = 10
    elif litera_index == 8:
        x = 400
        y = 200
        font_scale = 10
    elif litera_index == 9:
        x = 600
        y = 200
        font_scale = 10
    elif litera_index == 10:
        x = 800
        y = 200
        font_scale = 10
    elif litera_index == 11:
        x = 1010
        y = 200
        font_scale = 4
    elif litera_index == 12:
        x = 0
        y = 400
        font_scale = 10
    elif litera_index == 13:
        x = 200
        y = 400
        font_scale = 10
    elif litera_index == 14:
        x = 400
        y = 400
        font_scale = 10
    elif litera_index == 15:
        x = 600
        y = 400
        font_scale = 10
    elif litera_index == 16:
        x = 800
        y = 400
        font_scale = 10
    elif litera_index == 17:
        x = 1010
        y = 400
        font_scale = 4
   

    width = 200 #szerokość liter
    height = 200 #wysokośc liter
    th = 3 #grubość liter

#Ustawienia tekstu
    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_th = 4
    text_size = cv2.getTextSize(tekst, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
#Podświetlenie klawiszy
    if podswietlenie is True:
        cv2.rectangle(klawiatura, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
        cv2.putText(klawiatura, tekst, (text_x, text_y), font_letter, font_scale, (51, 51, 51), font_th)
    else:
        cv2.rectangle(klawiatura, (x + th, y + th), (x + width - th, y + height - th), (255, 0, 0), th)
        cv2.putText(klawiatura, tekst, (text_x, text_y), font_letter, font_scale, (255, 255, 255), font_th)
#Menu
def rys_menu():
    rows, cols, _ = klawiatura.shape
    th_lines = 4 # grubość linii
    cv2.line(klawiatura, (int(cols/2) - int(th_lines/2), 0),(int(cols/2) - int(th_lines/2), rows),
             (51, 51, 51), th_lines)
    cv2.putText(klawiatura, "LEWO", (160, 300), font, 6, (255, 255, 255), 5)
    cv2.putText(klawiatura, "PRAWO", (160 + int(cols/2), 300), font, 6, (255, 255, 255), 5)



def srodek(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

font = cv2.FONT_HERSHEY_PLAIN

#Zdefiniowanie funkcji do wykrywania mrugania
def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = srodek(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = srodek(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    
    ratio = hor_line_lenght / ver_line_lenght
    return ratio

#Zdefiniowanie funkcji konturów oczu
def kontury_oczu(facial_landmarks):
    left_eye = []
    right_eye = []
    for n in range(36, 42):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        left_eye.append([x, y])
    for n in range(42, 48):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        right_eye.append([x, y])
    left_eye = np.array(left_eye, np.int32)
    right_eye = np.array(right_eye, np.int32)
    return left_eye, right_eye
    
#Zdefiniowanie funkcji do wykrywania współczynnika spojrzenia
def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[7: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)
        
    right_side_threshold = threshold_eye[2: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio

#Liczniki
frames = 0
frames_prawa = 0
litera_index = 0
mruganie = 2
mruganie_prawa = 2
frames_to_blink = 6
frames_to_blink_prawa = 8
aktywna_ramka = 11


#Ustawienia tekstu i klawiatury
tekst = ""
zaznaczona_litera = True
wybrana_klawiatura = "lewo"
ostatnio_wybrana_klawiatura = "lewo"
wybor_menu = True
wybor_klawiatury = 0


while True:
    _, frame = cap.read()
    rows, cols, _ = frame.shape
    klawiatura[:] = (26, 26, 26)
    frames += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    #Rysowanie białej przestrzeni dla paska ładowania
    frame[rows - 50: rows, 0: cols] = (255, 255, 255)
    


    if wybor_menu is True:
        rys_menu()

    #Wybranie klawiatury
    if wybrana_klawiatura == "lewo":
        keys_set = ustawienie_klawiszy_1
    else:
        keys_set = ustawienie_klawiszy_2
    zaznaczona_litera = keys_set[litera_index]
    

    #Wykrywanie twarzy
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)

        left_eye, right_eye = kontury_oczu(landmarks)
        #right_eye = kontury_oczu(landmarks)

        #Wykrywanie mrugania
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
       # blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        #Kontur Oczu (Czerwony)
        cv2.polylines(frame, [left_eye], True, (0, 0, 255), 2)
        cv2.polylines(frame, [right_eye], True, (0, 0, 255), 2)

        if wybor_menu is True:
            #Wykrywanie spojrzenia, aby wybrać lewą lub prawą stronę klawiatury
            gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
            gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
            gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2

            if gaze_ratio <= 0.9:
                wybrana_klawiatura = "prawo"
                wybor_klawiatury += 1
                #Jeśli użytkownjik patrzy w jedną stronę więcej niż 15 klatek, przejdź do klawiatury
                if wybor_klawiatury == 15:
                    wybor_menu = False
                    prawo_dzwiek.play()
                    #Ustaw liczbę klatek na 0, gdy wybrana jest klawiatura
                    frames = 0
                    wybor_klawiatury = 0

                if wybrana_klawiatura != ostatnio_wybrana_klawiatura:
                    ostatnio_wybrana_klawiatura = wybrana_klawiatura
                    wybor_klawiatury = 0
           
            else:
                wybrana_klawiatura= "lewo"
                wybor_klawiatury += 1
                #Jeśli użytkownik patrzy w jedną stronę więcej niż 15 klatek, przejdź do klawiatury
                if wybor_klawiatury == 15:
                    wybor_menu = False
                    lewo_dzwiek.play()
                    #Ustaw liczbę klatek na 0, gdy wybrana jest klawiatura
                    frames = 0
                if wybrana_klawiatura != ostatnio_wybrana_klawiatura:
                    ostatnio_wybrana_klawiatura = wybrana_klawiatura
                    wybor_klawiatury = 0

        else:
            #Wykryj mruganie, aby wybrać klawisz, który się świeci
                if  right_eye_ratio  > 4.5:
                    mruganie_prawa += 1
                    frames_prawa -= 1
                    cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)
                    #cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
                    if  mruganie_prawa == frames_to_blink_prawa:
                        tekst = tekst[: -1]
                        tablica = np.zeros((100, 1400), np.uint8)
                        tablica [:] = 255
                else:
                    mruganie_prawa = 0          
                
                if  left_eye_ratio  > 5:
                    mruganie += 1
                    frames -= 1
                    #Pokaż zielony kontur oczu, gdy są zamknięte
                    cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
                    #cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)
                    
                    #Wpisywanie litery
                    if mruganie == frames_to_blink:
                        if zaznaczona_litera != "BACK" and zaznaczona_litera != "_" and zaznaczona_litera != "COPY" and zaznaczona_litera != "<-":
                            tekst += zaznaczona_litera
                        if zaznaczona_litera == "COPY":
                            okno.clipboard_clear()
                            okno.clipboard_append(tekst)
                            webbrowser.open('http://google.com/')
                        if zaznaczona_litera == "_":
                            tekst += " "
                        time.sleep(0.3) 
                        dzwiek.play()
                        wybor_menu = True  
                else:
                    mruganie = 0  

    #Pokaż tekst, który piszemy na tablicy
    cv2.putText (tablica, tekst, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 0, 0), 5) 
        
    #Wyświetlaj litery na klawiaturze
    if wybor_menu is False:
        if frames == aktywna_ramka:
            litera_index += 1
            frames = 0
        if litera_index == 18:
            litera_index = 0
        

        for i in range(18):
            if i == litera_index:
                light = True
            else:
                light = False
            litera(i, keys_set[i], light)     
    
    #Migający pasek ładowania
    percentage_blinking = mruganie_prawa / frames_to_blink_prawa
    loading_x = int(cols * percentage_blinking)
    cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (51, 51, 51), -1)
    
    cv2.imshow("Okno Kamery", frame)
    cv2.imshow("Wirtualna klawiatura", klawiatura)
    cv2.imshow("Tablica", tablica)
    #Wyłaczenie aplikacji
    key = cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

