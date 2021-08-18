file = []

def ask_input():
    return input("Choose a formatter: ")


def text(user):
    format_dict = {"plain": "", "bold": "**", "italic": "*", "inline-code": "`"}
    file.append(format_dict[user] + input('Text: ') + format_dict[user])
    show()


def new_line():
    file.append("\n")
    show()


def link():
    file.append(f"[{input('Label: ')}]({input('URL: ')})")
    show()


def header():
    lvl = int(input("Level: "))
    while not 1 <= lvl <= 6:
        print("The level should be within the range of 1 to 6")
        lvl = int(input("Level: "))
    file.append(f"{lvl * '#'} {input('Text: ')}\n")
    show()


def lists(l_type):
    while True:
        try:
            n_row = int(input("Number of rows: "))
            if n_row < 1:
                raise ValueError
            break
        except ValueError:
            print("The number of rows should be greater than zero")
    for l in range(n_row):
        if l_type == "ordered-list":
            file.append(f"{l + 1}. {input(f'Row #{l + 1}: ')}\n")
        else:
            file.append(f"* {input(f'Row #{l + 1}: ')}\n")


def help_():
    print("Available formatters: plain bold italic header link inline-code new-line\nSpecial commands: !help !done")


def show():
    print("".join(file))


def done():
    with open("output.md", "w") as f:
        f.write("".join(file))


def main():
    while True:
        user = ask_input()
        if user not in ["plain", "bold", "italic", "inline-code", "link", "header", "new-line", "ordered-list", "ordered-list" "!help", "!done"]:
            print("Unknown formatting type or command")
        if user in ["plain", "bold", "italic", "inline-code"]:
            text(user)
        if user == "header":
            header()
        if user == "link":
            link()
        if user == "new-line":
            new_line()
        if user in ["ordered-list", "unordered-list"]:
            lists(user)
            show()
        if user == "!help":
            help_()
        if user == "!done":
            done()
            break


if __name__ == "__main__":
    main()
