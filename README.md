## Usage

### Video Tutorial
Туториал можно найти здесь: [tutorial](https://drive.google.com/drive/folders/1MFamDDW4QaEAIImqnNOYolAeV8wRiubO?usp=sharing)
### Libs.
Чтобы установить нужные Python-библиотеки, достаточно либо иметь Python, установленный через Anaconda, либо через терминал вбить команду баша
```bash
 bash install_libs.sh
```
либо, если нет баша, просто ввести в терминал по порядку:
```
pip install numpy 
pip install pandas
```

### 1. 
Написать прогу на GPSS в файлик типа `gornostaev_4_gpss_no_mult.txt`.

 Там должна отсутствовать строка RMULT, потом скрипт нагенерит рандомных баз и для каждой базы сделает копию файла и положит в папку `gpss_experiment_scripts/`.
И сущности станков должны быть именованы либо STANOK<число> либо MACHINE<число>. Только тогда скрипт поймёт, что это станок, когда будет парсить файлы отчёта.
### 2.
 Затем использовать скрипт:
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
Самый занудный этап. Вручную просто копировать исходный код из сгенеренных файлов, подставлять в редактор GPSS, прогонять симуляцию, полученные отчеты сохранять по порядку в папку `reports/`. Нумерация - от единицы, так же как сгенеренные исходники.
 
 <b>ЛИБО</b> можно копировать и подставлять все отчёты в один файл и назвать его наподобие `merged_reports.txt`. 
Сохранять нужно в таком формате:
```
первый отчет
<>?
второй отчет
<>?
...
последний отчет
```
То есть, между отчетами должен быть разделитель "<>?". После последнего отчета не должно быть разделителя.

После того, как файл будет заполнен, использовать скрипт:
```bash
python split_reports.py merged_reports.txt reports/
```
также можно воспользоваться флагом -h, если нужно понять за что какой аргумент отвечает.

### 4.
 Использовать скрипт
```bash
$ python python_csv_fetcher.py reports/ --target_column_index 2 --n_sizes "5 20"
```
Также можно воспользоваться помощью -h
Первый аргумент в скрипт - папка с текстовыми отчетами прогона гыпыэсэс.
Второй аргемент - индекс колонки, которую надо обработать. 2, в данном случае, это UTILIZATION, он стоит по умолчанию.
Третий - размер массива для расчета средних и дисперсий в зависимости от размера выборки (по дефолту "5 20", можно не менять, если нужен просто отчёт)

### 5.
 Выводы в отчёт будут в папке `outputs/`. А именно: табличка средних и дисперсий, сырые данные, и таблички для каждого станка. Кроме того, в папке `reports/` (или как вы её решите назвать), файлы-отчёты из ГПСС будут обработаны: из них будут удалены лишние строки, вверху будут вставлены базы генераторов, которые были использованы в этом эксперименте, и эти файлы можно будет сразу вставлять в отчёт.


Скачать Anaconda можно [здесь](https://www.anaconda.com/products/individual)