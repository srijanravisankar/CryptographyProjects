# How to Run the Code

This C++ program is a single-file source code that can be compiled and executed using `g++`.

## Prerequisites
- Ensure you have `g++` installed. You can check by running:
  ```sh
  g++ --version
  ```
- If `g++` is not installed, you can install it using:
  - On Ubuntu/Debian:
    ```sh
    sudo apt update && sudo apt install g++
    ```
  - On macOS (via Homebrew):
    ```sh
    brew install gcc
    ```
  - On Windows (via MinGW):
    - Install MinGW from [mingw-w64.org](https://www.mingw-w64.org/)
    - Ensure `g++` is added to your system's PATH

## Compilation
To compile the program, run:
```sh
g++ -o program_name aes.cpp
```
Replace `program_name` with your desired executable name.

## Execution
To execute the compiled program:
```sh
./program_name
```