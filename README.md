Примеры 

(venv) muhammad@LAPTOP-ETLLARK3:~/TestLogReport/script$ python3 main.py --file example1.log example2.log  --report  average
+--------------------------+---------+---------------------+
| handler                  |   total |   avg_response_time |
+==========================+=========+=====================+
| /api/homeworks/...       |   55312 |               0.093 |
+--------------------------+---------+---------------------+
| /api/context/...         |   43928 |               0.019 |
+--------------------------+---------+---------------------+
| /api/specializations/... |    8335 |               0.052 |
+--------------------------+---------+---------------------+
| /api/challenges/...      |    1476 |               0.078 |
+--------------------------+---------+---------------------+
| /api/users/...           |    1447 |               0.066 |
+--------------------------+---------+---------------------+

2)(venv) muhammad@LAPTOP-ETLLARK3:~/TestLogReport/script$ python3 main.py --file example1.log   --report  average
+--------------------------+---------+---------------------+
| handler                  |   total |   avg_response_time |
+==========================+=========+=====================+
| /api/homeworks/...       |      71 |               0.158 |
+--------------------------+---------+---------------------+
| /api/context/...         |      21 |               0.043 |
+--------------------------+---------+---------------------+
| /api/specializations/... |       6 |               0.035 |
+--------------------------+---------+---------------------+
| /api/users/...           |       1 |               0.072 |
+--------------------------+---------+---------------------+
| /api/challenges/...      |       1 |               0.056 |
+--------------------------+---------+---------------------+

(venv) muhammad@LAPTOP-ETLLARK3:~/TestLogReport/script$ python3 main.py --file example1.log   --report  average --date 2025-22-06
+--------------------------+---------+---------------------+
| handler                  |   total |   avg_response_time |
+==========================+=========+=====================+
| /api/homeworks/...       |      71 |               0.158 |
+--------------------------+---------+---------------------+
| /api/context/...         |      21 |               0.043 |
+--------------------------+---------+---------------------+
| /api/specializations/... |       6 |               0.035 |
+--------------------------+---------+---------------------+
| /api/users/...           |       1 |               0.072 |
+--------------------------+---------+---------------------+
| /api/challenges/...      |       1 |               0.056 |
+--------------------------+---------+---------------------+

(venv) muhammad@LAPTOP-ETLLARK3:~/TestLogReport/script$ python3 main.py --file example1.log   --report  min
usage: main.py [-h] --file FILE [FILE ...] --report {average} [--date DATE]
main.py: error: argument --report: invalid choice: 'min' (choose from 'average')

(venv) muhammad@LAPTOP-ETLLARK3:~/TestLogReport/script$ python3 main.py --file unknown.log   --report  average
usage: main.py [-h] --file FILE [FILE ...] --report {average} [--date DATE]
main.py: error: argument --file: Файл не найден: unknown.log