# Coursework_ASM
Тема курсової роботи – Розробка компілятора програм мовою Асемблера. 
Основним завданням і результатом роботи програми компілятора повинно бути створення для програм мовою 
Асемблера текстового файла лістинга (розширення .lst), подібного до файла лістинга компілятора MASM або TASM. 
Враховуючи, що створення компілятора є трудомістким процесом, який потребує значних витрат часу, 
у варіантах завдань на курсову роботу використовуються суттєві обмеження на перелік допустимих машинних інструкцій, 
режимів адресації даних і команд та допустимих директив. Будь який із запропонованих студентам варіантів 
індивідуальних завдань фактично вказує на підмножину стандартної мови Асемблера процесорів фірми Intel. 
Тим не менш, цієї підмножини достатньо для забезпечення мети розробки. 

Варіант 17 (КВ-42):
Ідентифікатори
Містять великі і малі букви латинского алфавіту та цифри. Починаються з букви. Великі та малі букви не відрізняються. Довжина ідентифікаторів не більше 8 символів
Константи 
Шістнадцятерічні, десяткові, двійкові та текстові константи
Директиви
END,
SEGMENT - без операндів, ENDS, программа може мати тільки один сегмент кодів і тільки один сегмент даних
EQU
IF-ELSE-ENDIF
DB,DW,DD з одним операндом - константою (строкові константи тільки для DB)
Розрядність даних та адрес
32 - розрядні дані та зміщення в сегменті, 16 -розрядні дані та зміщення не використовуються
Адресація операндів пам'яті
Базова індексна адресація ([edx+esi],[ebx+ecx] і т.п.) з оператором визначення типу (ptr) при необхідності
Заміна сегментів
Префікси заміни сегментів можуть задаватись тільки явно
Машинні команди
movsd
Inc reg
Dec mem
Add reg,reg
Cmp reg,mem
And mem,reg
Mov reg,imm
Or mem,imm
Jbe
   
Де reg – 8 або 32-розрядні РЗП
mem – адреса операнда в пам’яті
imm - 8 або 32-розрядні безпосередні дані (константи)
