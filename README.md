Примеры приведу только с ошибками когда передают неверные данные, а обычные примеры почему то нормально не отображатся, ни скринами, ни текстом 



(venv) muhammad@LAPTOP-ETLLARK3:~/TestLogReport/script$ python3 main.py --file example1.log   --report  min
usage: main.py [-h] --file FILE [FILE ...] --report {average} [--date DATE]
main.py: error: argument --report: invalid choice: 'min' (choose from 'average')

(venv) muhammad@LAPTOP-ETLLARK3:~/TestLogReport/script$ python3 main.py --file unknown.log   --report  average
usage: main.py [-h] --file FILE [FILE ...] --report {average} [--date DATE]
main.py: error: argument --file: Файл не найден: unknown.log