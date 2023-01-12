# from threading import Thread
#
#
# def work(id, start, end, result):
#     total = 0
#     for i in range(start, end):
#         total += i
#     result.append(total)
#     return
#
#
# if __name__ == "__main__":
#     START, END = 0, 100000000
#     result = list()
#     th1 = Thread(target=work, args=(1, START, END, result))
#
#     th1.start()
#     th1.join()
#
# print(f"Result: {sum(result)}")
#
# from threading import Thread
#
# def work(id, start, end, result):
#     total = 0
#     for i in range(start, end):
#         total += i
#         print(id, total)
#     result.append(total)
#     return
#
# if __name__ == "__main__":
#     START, END = 0, 100000000
#     result = list()
#     th1 = Thread(target=work, args=(1, START, END//2, result))
#     th2 = Thread(target=work, args=(2, END//2, END, result))
#
#     th1.start()
#     th2.start()
#     th1.join()
#     th2.join()
#
# import threading
# import time
#
#
# class Worker(threading.Thread):
#     def __init__(self, name):
#         super().__init__()
#         self.name = name    # thread 이름 지정
#
#     def run(self):
#         print("sub thread start ", threading.currentThread().getName())
#         time.sleep(3)
#         print("sub thread end ", threading.currentThread().getName())
#
#
# print("main thread start")
# for i in range(5):
#     name = "thread {}".format(i)
#     t = Worker(name)    # sub thread 생성
#     t.start()           # sub thread의 run 메서드를 호출
#
# print("main thread end")
#
# import threading
# import time
#
#
# class Worker(threading.Thread):
#     def __init__(self, name):
#         super().__init__()
#         self.name = name    # thread 이름 지정
#
#     def run(self):
#         print("sub thread start", threading.currentThread().getName())
#         time.sleep(5)
#         print("sub thread end", threading.currentThread().getName())
#
#
# print("main thread start")
#
# threads = []
# for i in range(3):
#     thread = Worker(i)
#     thread.start()          # sub thread의 run 메서드를 호출
#     threads.append(thread)  # 쓰레드를 List에 담아서 관리하기
#
# for thread in threads:
#     thread.join()
#
# print("main thread post job")
# print("main thread end")
#
# import threading
# import time
#
#
# class Worker(threading.Thread):
#     def __init__(self, name):
#         super().__init__()
#         self.name = name                        # 이름 지정
#
#     def run(self):
#         print("sub thread start ", self.name)
#         time.sleep(3)
#         print("sub thread end ", self.name)
#
#
# print("main thread start")
# for i in range(5):
#     name = "thread {}".format(i)
#     t = Worker(name)                        # sub thread 생성
#     t.daemon = True
#     t.start()                               # sub thread의 run 메서드를 호출
#
# print("main thread end")
#
# import threading
# import time
#
# shared_number = 0
#
#
# def thread_1(number):
#     global shared_number
#     print("number = ", end=""), print(number)
#     for i in range(number):
#         shared_number += 1
#
#
# def thread_2(number):
#     global shared_number
#     print("number = ", end=""), print(number)
#     for i in range(number):
#         shared_number += 1
#
#
# if __name__ == "__main__":
#
#     start_time = time.time()
#     t1 = threading.Thread(target=thread_1, args=(50000000, ))
#     t1.start()
#
#     t2 = threading.Thread(target=thread_2, args=(50000000, ))
#     t2.start()
#
#     threads = [t1, t2]
#
#     for t in threads:
#         t.join()
#
#     print("--- %s seconds ---" % {time.time() - start_time})
#     print("shared_number=", end=""), print(shared_number)
#     print("end of main")
#
# import threading
# import time
#
# shared_number = 0
#
# lock = threading.Lock()
# def thread_1(number):
#     global shared_number
#     print("number = ", end=""), print(number)
#     for i in range(number):
#         lock.acquire()  # Lock 획득
#         shared_number += 1
#         lock.release()  # Lock 해제
#
# def thread_2(number):
#     global shared_number
#     print("number = ", end=""), print(number)
#     for i in range(number):
#         lock.acquire()  # Lock 획득
#         shared_number += 1
#         lock.release()  # Lock 해제
#
# if __name__ == "__main__":
#
#     start_time = time.time()
#     t1 = threading.Thread(target=thread_1, args=(50000000, ))
#     t1.start()
#
#     t2 = threading.Thread(target=thread_2, args=(50000000, ))
#     t2.start()
#
#     threads = [t1, t2]
#
#     for t in threads:
#         t.join()
#
#     print("--- %s seconds ---" % {time.time() - start_time})
#     print("shared_number=", end=""), print(shared_number)
#     print("end of main")
#
# from time import strftime, localtime
#
# tm = localtime
# print(strftime('%I:%M'))
# print(type(strftime('%I:%M')))
import datetime

# print(datetime.datetime.today().weekday())
print(datetime.datetime.today() - datetime.timedelta(1))
print(datetime.date.today() - datetime.timedelta(2))
# print(datetime.datetime.now())
# today = datetime.date.today()
# target_date = datetime.date(2023, 5, 24)
# holiday = [datetime.date(2023, 1, 22), datetime.date(2023, 1, 21)]
# print(datetime.date.weekday() in (target_date - today))
print(str(datetime.date.today()))