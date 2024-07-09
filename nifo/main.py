import argparse
from pathlib import Path
from nifo.file_scanner import FileScanner
from nifo.analyzer import Analyzer
from nifo.display import Display
from nifo.config_detector import ConfigDetector

def main():
    parser = argparse.ArgumentParser(description="nifo: Code Information Tool")
    parser.add_argument("directory", type=str, help="Directory to analyze")
    parser.add_argument("-a", "--all", action="store_true", help="Include hidden files and ignore .gitignore")
    parser.add_argument("-l", "--language", type=str, help="Filter by programming language")
    parser.add_argument("-v", "--verbose", action="store_true", help="Display detailed logs")
    parser.add_argument("-b", "--count-binary", action="store_true", help="Count binary and image files")
    args = parser.parse_args()

    directory = Path(args.directory)
    if not directory.is_dir():
        print(f"Error: {directory} is not a valid directory")
        return

    file_scanner = FileScanner(directory, include_hidden=args.all, count_binary=args.count_binary)
    files = file_scanner.scan()

    analyzer = Analyzer(files)
    results = analyzer.analyze()

    if args.language:
        results = {k: v for k, v in results.items() if k.lower() == args.language.lower()}

    config_detector = ConfigDetector(directory)
    config_files = config_detector.detect()

    display = Display(results, config_files, file_scanner.binary_count, file_scanner.image_count, verbose=args.verbose)
    display.show()

if __name__ == "__main__":
    main()