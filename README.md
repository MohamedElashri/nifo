# nifo: Code Information Tool

## Description

`nifo` is a command-line tool designed to provide detailed information about code in a specified directory and its subdirectories. It analyzes your codebase, offering insights into the languages used, lines of code, comments, and more. `nifo` respects `.gitignore` files and can identify configuration and potential secret files.

This tool is currently in development and is designed to be simple yet effective for developers who want a quick overview of their project structure and composition.

## Features

- Calculates total lines of code, lines without comments, and comment lines for each detected language
- Detects and reports on programming languages used in the project
- Respects `.gitignore` files to exclude ignored files and directories
- Identifies configuration and potential secret files
- Automatically ignores common non-code files and directories (e.g., LICENSE, README, .git, node_modules, etc.)
- Option to include or exclude hidden files
- Filters results by programming language
- Counts binary and image files (optional)
- Provides percentage breakdown of language usage in the project

## Installation

Currently, `nifo` is not available on PyPI. To install, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/MohamedElashri/nifo
   ```

2. Navigate to the project directory:
   ```
   cd nifo
   ```

3. Install the package in editable mode:
   ```
   pip install -e .
   ```

## Usage

Basic usage:

```
nifo [options] <directory>
```

### Example Usage

Analyze the current directory:
```
nifo .
```

Analyze a specific directory, including hidden files:
```
nifo -a /path/to/your/project
```

Analyze only Python files in a directory:
```
nifo -l python /path/to/your/project
```

### Options

- `-a, --all`: Include hidden files and ignore `.gitignore` rules. By default, hidden files are excluded and `.gitignore` rules are respected.

- `-l LANGUAGE, --language LANGUAGE`: Filter results to only include the specified programming language. For example, `-l python` will only show results for Python files.

- `-v, --verbose`: Display detailed logs, including a list of detected configuration and potential hidden files.

- `-b, --count-binary`: Include a count of binary and image files in the output. By default, these files are ignored in the main analysis.

- `-h, --help`: Display the help message and exit.

## Output

`nifo` provides a table output with the following columns:

- **Language**: Detected programming language
- **Files**: Number of files for each language
- **Total Lines**: Total number of lines (including comments and blank lines)
- **Code Lines**: Number of lines containing code
- **Comment Lines**: Number of lines containing comments
- **% of Codebase**: Percentage of the total codebase this language represents

Additionally, it reports:
- **Number of binary files** (if --count-binary option is used)
- **Number of image files** (if --count-binary option is used)
- **List of configuration and potential hidden files** (in verbose mode)

## Limitations

- Language detection is based on file extensions and may not be 100% accurate for all file types.
- Comment detection is simplistic and may not accurately capture all comment styles across different languages.
- Binary and image file detection is based on file extensions and basic content checks, which may not be comprehensive.
- Some common project files (like README, LICENSE) are ignored by default. Use the `-a` flag to include these if needed.

## Contributing

Contributions to `nifo` are welcome! Please feel free to submit pull requests, create issues, or suggest new features.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Disclaimer

`nifo` is a simple tool and is currently under active development. It may contain bugs or limitations. Use at your own discretion and always verify important results manually.
