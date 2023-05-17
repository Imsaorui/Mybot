import subprocess
import threading

def extract_printed_text(command, callback):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    def read_output():
        for line in iter(process.stdout.readline, ''):
            line = line.rstrip()  # 去除行尾的换行符
            callback(line)  # 将每一行输出传递给回调函数

    output_thread = threading.Thread(target=read_output)
    output_thread.start()

    process.wait()
    output_thread.join()

def process_output(line):
    # 在这里对每一行输出进行处理
    print("Processing:", line)

# 示例命令：在命令行每秒打印一次时间
command = 'python -c "import time; i = 0; while i < 5: print(time.ctime()); time.sleep(1); i += 1"'

# 提取实时打印的文本并传递给其他函数进行处理
extract_printed_text(command, process_output)