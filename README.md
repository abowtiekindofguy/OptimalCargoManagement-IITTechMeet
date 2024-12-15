# Optimal Cargo Management - FedEx (Team 32)
This is IIT Delhi's submission for the 13th Inter IIT Tech Meet. The goal was to pack packages into Unit Loading Devices as efficiently as possible while retaining sufficient generalization for unseen data.

Joint work with Arpit Agrawal and Kushagra Gupta

## Running the Code

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

This command will execute `main.py` with the provided arguments. Any logs will be saved to `log.txt`. Note that you can access the logs only after the script has finished executing. Also, the `verbose` argument can be set to `0` or `1`to control the verbosity level.

After the execution of the script, solution would be obtained in `output_file_path` and a graphic would be saved for each of the ULDs.

### Visualizing the Output

To visualize the output, you can use the following command:

```bash
make visualize input=<input_file_path> output=<output_file_path>
```

For example:

```bash
make visualize input=data/input.txt output=data/output.txt
```

This command will display the output using a visualization tool powered by MatPlotLib. The visualization will be displayed in a new window titled "Optimal Cargo Management - FedEx". Also, a png graphic would be saved for the visualization with a particular default projection.

### Troubleshooting

- If the `input`, `output`, or `verbose` arguments are not provided, the script will display an error message indicating the first argument that is missing.

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
