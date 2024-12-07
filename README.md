# Project Title

A brief description of your project, its purpose, and key features.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

---

## Installation

### Prerequisites

Ensure you have `pip3` installed to manage Python packages.

### Setting up the Environment

To install the required dependencies, run the following command:

```bash
make setup
```

This will:
1. Install all dependencies listed in `requirements.txt` using `pip3`.

### Optional: Install Dependencies Manually

If you prefer to install the dependencies manually without using `Makefile`, you can run:

```bash
pip3 install -r requirements.txt --break-system-packages
```

## Usage

Once the dependencies are installed, you can run the Python script with the required arguments. The script expects the following arguments:

- **input**: The path to the input file (required).
- **output**: The path to the output file (required).
- **verbose**: The verbosity level (required).

### Running the Script

To run the script, use the following command:

```bash
make run input=<input_file_path> output=<output_file_path> verbose=<verbose_level>
```

For example:

```bash
make run input=data/input.txt output=data/output.txt verbose=1
```

This command will execute `main.py` with the provided arguments. Any logs will be saved to `log.txt`.

### Troubleshooting

- If the `input`, `output`, or `verbose` arguments are not provided, the script will display an error message indicating which argument is missing.

## License

MIT License

Copyright (c) [2024] [Team Number 32]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
