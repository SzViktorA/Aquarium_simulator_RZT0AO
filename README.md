# Akvárium Szimulátor — Szabó Viktor Attila (RZT0AO)

## Program leírása:

A program egy egyszerű akvárium szimulátor, amelyben kétféle hal úszkál a képernyőn:
Prey (menekülő hal): elmenekül az egér elől.
Predator (ragadozó hal): véletlenszerűen úszik, és ha az egér túl közel kerül hozzá, „megeszi” azt.
A program újraindítható az R billentyűvel, illetve ESC-kel kiléphető.
A kurzor helyett egy „ujj” ikon jelenik meg, mintha a játékos a vízbe nyúlna.

### Modulok és függvények
	main.py
	A program indításáért felel.
	Meghívja az app.run_app() függvényt.

	app.py
	Tartalmazza a grafikus felület és a fő játékhurok logikáját.
	Főbb függvények:
	load_background_VS() – háttérkép betöltése vagy alap háttér generálása.
	create_fish_list_VS() – halak létrehozása véletlenszerűen, legalább egy ragadozó és egy préda.
	run_app() – a fő játéklogika, eseménykezelés, képernyőfrissítés.

	fishmodul_VS.py
	Saját modul, amely tartalmazza a halak viselkedését és mozgását.
	Főbb elemek:
	class Fish_VS – saját osztály a hal objektumhoz (pozíció, sebesség, típus, mozgás, kirajzolás).
	check_mouse_proximity_VS() – ellenőrzi, hogy az egér közel van-e a ragadozóhoz.
	create_random_fish_VS() – véletlenszerű halak generálása, mindkét típusból legalább egy.

	bubblemodul_VS.py
 	Buborék animációk kezelése.
	 Főbb elemek:
    	 class Bubble_MG  
    	   __init__(x, y, radius=None, speed=None) — létrehoz egy buborékot.  
    	   update() — frissíti a pozíciót és átlátszóságot (felúszás).  
    	   draw(screen) — kirajzolja a buborékot (transzparens felületen).  
    	   is_dead(screen_height) — visszaadja, ha a buborék eltűnt/kiment a képernyőről.

***Osztályok***
	Fish_VS
	Attribútumok: x, y, vx, vy, image, fish_type, rect, flipped.
	Metódusok:
	move() – a hal mozgását kezeli, elkerüli a képernyő szélét, és reagál az egér közelségére.
	draw() – kirajzolja a halat a képernyőre.

***Egyéb funkciók:***

- Alternatív kurzor (emberi ujj kép).
- Hanghatás, amikor a hal „megeszi” az egeret.
- Buborék animáció a háttérben.

***Futtatás:***

1. Helyezd az összes fájlt ugyanabba a mappába.
2. Legyen egy assets mappa a képekkel és hanggal (pl. fish1.png, fish2.png, finger.png, chomp.mp3).
3. Indítsd el a programot:
python main.py
