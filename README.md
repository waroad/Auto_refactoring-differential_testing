
# Auto_refactoring-differential_testing

This project refactors non-Pythonic Python code to make it more Pythonic. It also generates as many test cases as possible to verify that the functionality remains the same before and after refactoring.

## Participants
- Doha Nam: [https://github.com/waroad](https://github.com/waroad)
- Seongwon Jeong: [https://github.com/JeongSeongwon99](https://github.com/JeongSeongwon99)
- Hyeonsu Lee: [https://github.com/2eehyun](https://github.com/2eehyun)
- Minho Cha: [https://github.com/Cha-Minho](https://github.com/Cha-Minho)

Since external libraries such as the z3 solver are used, please download the necessary libraries.
```sh
pip install -r requirements.txt
```

## Usage
First, put all the Python files you want to refactor into a single folder. The internal structure of the folder does not matter.

```
example/
├── simple/
│   ├── simple1.py
│   └── simple2.py
```

Create a folder to contain the refactored code.

```
updated/
```

### Refactoring and Differential Testing
```sh
python main.py -t1 example -t2 updated
```

### Refactoring Only
```sh
python refactor.py -t1 example -t2 updated
```

### Differential Testing Only
```sh
python diff_testing.py -t1 example -t2 updated
```
