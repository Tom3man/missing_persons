import sys


def main():

    folder_path = '../'
    sys.path.append(folder_path)

    from missing_individuals.missing_persons.src.run import \
        main as missing_persons_run
    missing_persons_run()


if __name__ == "__main__":
    main()
