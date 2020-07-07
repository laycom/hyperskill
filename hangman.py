from random import choice


def hangman():
    life = 8
    secret_words = ['python', 'java', 'kotlin', 'javascript']
    secret_word = list(choice(secret_words))
    hidden_word = ['-' for _ in range(len(secret_word))]
    user_letters = []

    while life > 0:
        print()
        print(''.join(hidden_word))
        user_letter = input('Input a letter: ')

        if len(user_letter) != 1:
            print("You should input a single letter")
        elif user_letter.isupper() or not user_letter.isalpha():
            print("It is not an ASCII lowercase letter")
        elif user_letter in user_letters:
            print("You already typed this letter")
        elif user_letter in secret_word:
            for j in range(len(secret_word)):
                if user_letter == secret_word[j]:
                    hidden_word[j] = secret_word[j]
        else:
            print("No such letter in the word")
            life -= 1

        user_letters.append(user_letter)

        if hidden_word == secret_word:
            print(f"You guessed the word {''.join(hidden_word)}!")
            print("You survived!")
            break
    else:
        print("You are hanged!")


def main():
    print("H A N G M A N")
    while True:
        command = input('Type "play" to play the game, "exit" to quit: ')
        if command == 'play':
            hangman()
        elif command == "exit":
            break


if __name__ == '__main__':
    main()


