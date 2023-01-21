import os


def main():
    # Modify id_str based on your needs
    id_str = "Kopie"

    # Keeps track of deleted files
    del_count = 0

    # Control output verbosity
    verbose = False


    # Delete all files containing id_str in the current directory and sub directories
    for root, dirs, files in os.walk("."):
        for file in files:
            if id_str in file:
                try:
                    os.remove(os.path.join(root, file))
                    if verbose:
                        print("[+] Deleted file: " + os.path.join(root, file))
                    del_count += 1
                except Exception as e:
                    print("[!] Error deleting file: " + os.path.join(root, file) + " - you may delete the file manually.")
                    continue

    print("[+] Successfully deleted " + str(del_count) + " files")


if __name__ == '__main__':
    main()

