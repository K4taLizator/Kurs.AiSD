from hashlib import md5, sha1, sha256, sha3_256, blake2b, blake2s
import time
import sys
import string
import matplotlib.pyplot as plt

def progress_bar(iteration, total, length=40):
    # Вычисляем процент завершения
    percent = (iteration / total)
    # Вычисляем количество символов для заполнения прогресс-бара
    filled_length = int(length * percent)
    # Создаем строку прогресс-бара
    bar = '█' * filled_length + '-' * (length - filled_length)
    # Выводим прогресс-бар
    sys.stdout.write(f'\r|{bar}| {percent:.2%} Complete')
    sys.stdout.flush()

def brute_force(hash, total=10e7):
    start = time.time()
    progress_bar(1, total)
    for i in range(total):
        if i %20000 == 0:
            progress_bar(i, total)
        if hash == md5(str(i).encode('utf-8')).hexdigest():
            print("Input password:", end = "")
            print(i)
            break
    end = time.time()
    print("Time for bruteforce" + str(end - start))

def dict_scan(hash, file_path):
    start = time.time()
    ex = dict()
    k = 0
    file = open(file_path, 'r', encoding='utf-8').readlines()
    total = len(file)
    progress_bar(1, total)
    for i in file:
        ex[md5(i[:-1].encode('utf-8')).hexdigest()] = i
        k+=1
        if k %20000 == 0:
            progress_bar(k, total)
    mid = time.time()
    try:
        print('\nThe password was:'+ ex[hash])
    except:
        print(f"\npassword not found in dict\n Hash: {hash}")
    end = time.time()
    print("Time making dict:" + str(mid - start))
    print("Time scan password:" + str(end - mid))

def reduce(hash_value, length=6):
    """Функция редукции, которая преобразует хеш в строку фиксированной длины."""
    # Преобразуем хеш в число
    num = int(hash_value, 16)

    # Доступные символы для генерации паролей
    characters = string.digits + string.ascii_letters

    # Генерация строки фиксированной длины
    reduced = ''
    while len(reduced) < length:
        # Получаем индекс символа из числа
        index = num % len(characters)
        reduced += characters[index]
        num //= len(characters)

    return reduced

def line_attempt(inp, attempt):
    for i in range(attempt):
        hash = md5(inp.encode('utf-8')).hexdigest()
        inp = reduce(hash)
    return inp

def rainbow_scan(hash, file_path, attempt=2):
    start = time.time()
    ex = dict()
    k = 0
    file = open(file_path, 'r', encoding='utf-8').readlines()
    total = len(file)
    progress_bar(1, total)
    for i in file:
        ex[md5(line_attempt(i[:-2], attempt).encode('utf-8')).hexdigest()] = i[:-2]
        k+=1
        if k %20000 == 0:
            progress_bar(k, total)
    mid = time.time()
    for i in range(10):
        if hash in ex.keys():
            inp = line_attempt(ex[hash], attempt-i)
            print('\nThe Password was: ' + inp)
            end = time.time()
            print("Time making rainbow:" + str(mid - start))
            print("Time scan password:" + str(end - mid))
            return 1
        else:
            hash = md5(reduce(hash).encode('utf-8')).hexdigest()
    print('\nThe Password not found')
    end = time.time()
    print("Time making rainbow:" + str(mid - start))
    print("Time scan password:" + str(end - mid))

def test_hash_time(file_path, hash):
    file = open(file_path, 'r', encoding='utf-8').readlines()
    total = len(file)
    s = ""
    k = 0
    res = 200
    times = []
    s = ' '.join(list(file))
    progress_bar(0, res)
    k = 0
    for i in range(total//res, total+1, total//res):
        st = time.time()
        hash(s[0:i].encode('utf-8'))
        end = time.time()
        times.append(end-st)
        progress_bar(k, res)
        k+=1
    progress_bar(res, res)
    fig = plt.figure()
    plt.plot([i*total//res for i in range(len(times))], times, 'r')
    a = hash('111'.encode('utf-8'))
    #plt.scatter([i*total//res*3 for i in range(len(times[::3]))], times[::3], marker='*')
    plt.title(f"Estimated time {a.name}")
    plt.xlabel('Input words')
    plt.ylabel('Time')
    plt.grid()
    plt.show()
    

def main():
    print("Input password: ", end = "")
    password = input().encode('utf-8')
    hash = str(md5(password).hexdigest())
    #brute_force(hash, 10000000)
    #dict_scan(hash,'C:\\Users\\user\\Desktop\\1234\\ignis-10M.txt')
    #rainbow_scan(hash, 'C:\\Users\\user\\Desktop\\1234\\ignis-10M.txt')
    test_hash_time('C:\\Users\\user\\Desktop\\1234\\ignis-10M.txt', md5)
    test_hash_time('C:\\Users\\user\\Desktop\\1234\\ignis-10M.txt', sha1)
    test_hash_time('C:\\Users\\user\\Desktop\\1234\\ignis-10M.txt', sha256)
    test_hash_time('C:\\Users\\user\\Desktop\\1234\\ignis-10M.txt', sha3_256)
    test_hash_time('C:\\Users\\user\\Desktop\\1234\\ignis-10M.txt', blake2b)
    test_hash_time('C:\\Users\\user\\Desktop\\1234\\ignis-10M.txt', blake2s)
    
main()