from ListingsPreprocessor.engine import ImagesPrepocessor, SheetsWork
import time

def print_format_time(running_time):
    minutes = int(running_time // 60)
    seconds = int((running_time % 1) * 60)
    mins = "mins" if minutes > 1 else "min"
    secs = "secs" if seconds > 1 else "sec"

    print(f"Running time: {minutes}{mins} {seconds}{secs}")


if __name__ == "__main__":
    input_directory = "./Listings_Pictures/originals"
    output_directory = "./Listings_Pictures/mods"

    start_time = time.perf_counter()
    ImagesPrepocessor.run(input_directory, output_directory)
    SheetsWork.run()
    end_time = time.perf_counter()

    running_time = end_time - start_time

    print_format_time(running_time)
