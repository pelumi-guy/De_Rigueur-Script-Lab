import os
import shutil
from ListingsPreprocessor.engine import SheetsWork

input_dir = "./Listings_Pictures/originals"
target = "./Listings_Pictures/old"

def Run():
    active_listings = SheetsWork.extract_active_listings()
    all_listings = []

    for images_dir in os.listdir(input_dir):
        all_listings.append(images_dir)

    set1 = set(all_listings)
    set2 = set(active_listings)

    # Find elements that are in one set but not in the other
    old_listings = list(set1.symmetric_difference(set2))
    unused_dirs = ", ".join(old_listings)


    # print("All listings:", all_listings)
    # print("Active listings:", active_listings)
    # print("Old listings:", old_listings)

    for directory in old_listings:
        dir_name = os.path.join(input_dir, directory)
        shutil.move(dir_name, target)

    print("Unused listing pictures folders found:", unused_dirs)


if __name__ == "__main__":
    Run()
    print("All unused listing pictures folders have been cleaned successfully.")