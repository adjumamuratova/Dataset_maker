# tensorflow_dataset_maker

1. Запустить main.py, в командной строке:
	python main.py
2. В папкe, где будут храниться TF.record, создать папки annotations/xmls, images, images_with_label:
	|-annotations
	||-xmls
	| - images
	| - images_with_label
3. Выбрать Directory to xml.
4. С помощью мыши разметить изображение (инициализация трекера после того, как отпустим), в полях Frequency xmls и Object class можно назначить частоту записи
   xml-файлов и класс объекта.
5. Когда запись xml-файлов не происходит - появляется красная надпись "XMLS ARE NOT CREATING".
6. Горячая клавиша переключения play/pause - Enter
7. Горячая клавиша "create_xml" - F12
8. По умолчанию разметка идет трекером, но можно переключиться в режим ручной разметки - "Label img"
9. В режиме ручной разметки можно разметить сразу несколько объектов, при указании "Object class" необходимо нажать
   Tab или щелкнуть мышью по другому полю.
   ЕСЛИ НУЖНО НА ОДНОМ КАДРЕ РАЗМЕТИТЬ РАЗНЫЕ КЛАССЫ ОБЪЕКТОВ, ТО НУЖНО МЕНЯТЬ ИМЯ КЛАССА (И НАЖАТЬ TAB) ДО ТОГО, КАК НАКИДЫВАТЬ РАМКУ!
10. После вызова "Save XML" сохраняются соответствующие файлы и происходит переход к следующему кадру.
11. Горячая клавиша "Save XML" - F11.

