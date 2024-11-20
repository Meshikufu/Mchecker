import datetime
import traceback


def error_logger():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open('error_log.txt', 'a') as file:
        file.write("\n")
        file.write(f"Date and Time: {current_time}\n")
        file.write("Traceback (most recent call last):\n")
        traceback.print_exc(file=file)  # This prints the full traceback to the file