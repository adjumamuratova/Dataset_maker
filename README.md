# tensorflow_dataset_maker

1. Установить python 3.6.6 https://www.python.org/downloads/release/python-366/
2. Вставить Path (переменные среды пользователя для user) пути к python.exe и pip.exe, например:
	C:\Users\User\AppData\Local\Programs\Python\Python36
	C:\Users\User\AppData\Local\Programs\Python\Python36\Scripts
3. В командной строке ввести следующие команды:
	pip install opencv-python
	pip install opencv-contrib-python
	pip install shutil
	pip install PyQt5
4. Запустить main.py, в командной строке:
	python main.py
5. В папкe, где будут храниться TF.record, создать папки annotations/xmls, images, images_with_label:
	|-annotations
	||-xmls
	| - images
	| - images_with_label
6. Выбрать Directory to xml.
7. С помощью мыши разметить изображение (инициализация трекера после того, как отпустим), в полях Frequency xmls и Object class можно назначить частоту записи
   xml-файлов и класс объекта.
8. Когда запись xml-файлов не происходит - появляется красная надпись "XMLS ARE NOT CREATING".
9. Горячая клавиша переключения play/pause - Enter
10. Горячая клавиша "create_xml" - F12
11. По умолчанию разметка идет трекером, но можно переключиться в режим ручной разметки - "Label img"
12. В режиме ручной разметки можно разметить сразу несколько объектов, при указании "Object class" необходимо нажать
   Tab или щелкнуть мышью по другому полю.
   ЕСЛИ НУЖНО НА ОДНОМ КАДРЕ РАЗМЕТИТЬ РАЗНЫЕ КЛАССЫ ОБЪЕКТОВ, ТО НУЖНО МЕНЯТЬ ИМЯ КЛАССА (И НАЖАТЬ TAB) ДО ТОГО, КАК НАКИДЫВАТЬ РАМКУ!
13. После вызова "Save XML" сохраняются соответствующие файлы и происходит переход к следующему кадру.
14. Горячая клавиша "Save XML" - F11.

