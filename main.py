import pyautogui
import webbrowser
import random
from guesser import KatlaGame

# membuat angka acak
random_seed: int = random.randint(1, 1122)

def run(website_url) -> None:
    """
    Membuka web browser dan pergi ke url https://katla.id/arsip/{angka acak}
    """
    webbrowser.open(url=website_url)
    pyautogui.doubleClick(None, None, 0.3, 'left')

def main() -> None:
    """
    Menjalankan program
    """
    url: str = f'https://katla.id/arsip/{random_seed}' # menghasilkan link acak
    run(url)

    game = KatlaGame("wordlist.txt")
    game.play()

if __name__ == '__main__':
    main()