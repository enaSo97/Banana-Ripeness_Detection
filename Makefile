all: main dependencies

dependencies: src/imageIO.py src/imthr_lib.py
	chmod u+x src/imageIO.py
	chmod u+x src/imthr_lib.py 

main: src/main.py
	chmod u+x src/main.py

clean:
	rm images/processed/*.png
	rm images/brownSpot/ripe/*.png
	rm images/brownSpot/very_Ripe/*.png
	rm images/brownSpot/over_Ripe/*.png
	rm images/brownSpot/yellowed/*.png
	rm images/brownSpot/un_Ripe/*.png
	rm images/brownSpot/not_Banana/*.png
	rm src/*.pyc

