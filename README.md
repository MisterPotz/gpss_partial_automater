## Usage

### 1. 
Написать прогу на GPSS в файлик типа `gornostaev_4_gpss_no_mult.txt`.

 Там должна отсутствовать строка RMULT, потом скрипт нагенерит рандомных баз и для каждой базы сделает копию файла и положит в папку gpss_experiment_scripts.

### 2.
 Использовать скрипт, типа как тут
```bash
python gpss_files_generator.py 20 5 gornostaev_4_gpss_no_mult.txt
```
gpss_files_generator.py - консольное приложение, можно воспользоваться помощью
```bash
$ python gpss_files_generator.py -h 
```
чтобы понять, что туда передаётся.
После выполнения команды будут сгенерированы файлы-исходники модели GPSS для разных RMULT. 

### 3. 
Самый занудный этап. Вручную просто копировать исходный код из сгенеренных файлов, подставлять в редактор GPSS, прогонять симуляцию, полученные отчеты сохранять по порядку в папку reports/.
Нумерация - от единицы, так же как сгенеренные исходники.

### 4.
 Использовать скрипт
```bash
$ python python_csv_fetcher.py reports/ --target_column_index 2 --n_sizes "5 20"
```
Также можно воспользоваться помощью -h
Первый аргумент в скрипт - папка с текстовыми отчетами прогона гыпыэсэс.
Второй аргемент - индекс колонки, которую надо обработать. 2, в данном случае, это UTILIZATION.
Третий - размер массива для расчета средних и дисперсий в зависимости от размера выборки (по дефолту "5 20", для просто отчета можно не менять)
### 5.
 Выводы в отчёт будут в папке outputs.

Использован Python 3.7 (3.8 тоже должен работать), все библиотеки стандартные, которые идут в комплекте с Anaconda.
Скачать Anaconda можно [здесь](https://www.anaconda.com/products/individual)ы