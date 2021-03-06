# code_task5
Проект содержит следующие классы

* CodeCreator - класс, генерирующий код с заданными параметрами n и p, причём n увеличивается до ближайшего сверху числа, равного 2^m - 1

* Encoder - класс, осуществляющий кодирование сообщения и наложения шума с заданной вероятностью

* Decoder - класс, осуществляющий декодирование сообщения

* Help - класс со вспомогательными функциями

* Combinatorics - класс со вспомогательными функциями комбинаторики

* Poly - класс для работы с многочленами над полем GF(2)

* pyfinite - класс для работы с расширениями конечных полей. Реалиазацию взял отсюда:

  https://github.com/emin63/pyfinite

Проект допускает 3 режима:

* Режим 1 (mode=1) или режим генерации кода

* Режим 2 (mode=2) или режим кодирования и наложения шума

* Режим 3 (mode=3) или режим декодирования

## Режим 1

Чтобы сгенерировать БЧХ-код с парамтрами n и p запустите:

  python3 main.py mode=1 n p out_inf.txt

где:

* n - размер блока

* p - вероятность ошибки двоичного симметричного канала

* out_inf.txt - файл, куда записывается необходимая информация для кодера и декодера

Программа выводит значения для поля GF(2^m):

* size - длина получившегося блока сообщения, size = 2^m - 1

* m - степень

* k - размер сообщения (получается из неравенства Варшамова-Гильберта)

* d - кодовое расстояние (получается из неравенства Варшамова-Гильберта и границы Синглтона)

* t - число ошибок, исправляемых кодом

* p - вероятность ошибки двоичного симметричного канала

* deg - степень порождающего многочлена

* массив с коэфициентами порождающего многочлена

### Пример работы

    python3 main.py mode=1 13 0.125 code_info/code.txt

генерирует БЧХ-код со следующими параметрами GF(2^4):

* m = 4

* k = 6

* r = 9

* d = 5

* t = 2

* p = 0.125

* deg = 8

* 1 0 0 0 1 0 1 1 1 0 0 0 0 0, то есть порождающий многочлен равен: g(x) = 1+x^4+x^6+x^7+x^8

* записывает эти параметры в файл code_info/code.txt.

### Алгоритм работы

1 Параметры k, d и n выбираются из неравенства Варшамова-Гильберта и границы Синглтона.

2 Строится поле из 2^m элементов.

3 В зависимости от кодового расстояния (d) строятся минимальные многочлены и порождающий многочлен.


## Режим 2

Чтобы закодировать сообщение из файла text.txt БЧХ-кодом и получить зашумлённое и незашёмлённое закодировнные сообщения запустите:

  python3 main.py mode=2 code_info/code.txt text.txt encode_text/encode_noise_text.txt encode_text/encode_text.txt

где:

* code_info/code.txt - файл с описанием БЧХ-кода

* text.txt - файл с сообщением

* encode_text/encode_noise_text.txt - файл с зашумлённым закодированным сообщением при помощи БЧХ-кода на основе вероятности p

* encode_text/encode_text.txt - файл с незашумлённым закодированным сообщением при помощи БЧХ-кода

## Режим 3

Чтобы декодировать сообщение на основе восстановления линейного регистра сдвига алгоритмом Берлекэмпа-Месси запустите:

  python3 main.py mode=3 code_info/code.txt encode_text/encode_text.txt decode_text/decode_text.txt

где:

* code_info/code.txt - файл с описанием БЧХ-кода

* encode_text/encode_text.txt - файл с закодированным сообщением

* decode_text/decode_text.txt - файл, в который записывается декодированное сообщение

# Результаты экспериментов

Для проверки работы программы генерировался код (Пример к режиму 1) при запуске:

    python3 main.py mode=1 13 0.125 code_info/code.txt

Кодирование осуществлялось при запуске:

    python3 main.py mode=2 code_info/code.txt text.txt encode_text/encode_noise_text.txt encode_text/encode_text.txt

Получившиеся сообщение в файле encode_text/encode_noise_text.txt содержит больше, чем 2 ошибки в некоторых блоках.

## Случай с количеством ошибок, большим, чем 2 в блоках

Декодирование осуществлялось сообщения из файла encode_text/encode_noise_text.txt, содержащего блоки с более, чем двумя ощибками. Запуск программы:

    python3 main.py mode=3 code_info/code.txt encode_text/encode_noise_text.txt decode_text/decode_noise_text.txt

Декодирование осуществляется неверно, и сообщение в файле decode_text/decode_noise_text.txt не равно исходному сообщению из файла text.txt.


## Случай с количеством ошибок, не более, чем 2 в каждом блоке

Декодирование осуществлялось сообщения из файла encode_text/encode_noise_correct_text.txt, содержащего блоки с не более, чем двумя ощибками. Запуск программы:

    python3 main.py mode=3 code_info/code.txt encode_text/encode_noise_correct_text.txt decode_text/decode_noise_correct_text.txt

Декодирование осуществляется верно, и сообщение в файле decode_text/decode_noise_correct_text.txt равно исходному сообщению из файла text.txt.
