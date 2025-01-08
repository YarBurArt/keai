from playwright.sync_api import sync_playwright
from playwright._impl._api_types import TimeoutError
from keai.chatKeai2 import run


if __name__ == '__main__':
    out_text = "hello"
    with open('../data/rei_faketext.txt', 'a') as file:
        for i in range(1000):
            message = out_text
            try:
                with sync_playwright() as playwright:
                    out_text = run(playwright, message)
                    file.write(out_text)
                    print(out_text)
                    out_text = run(playwright, out_text,
                                   chara_id="mWlPN3NU6GyyZKUiV93bfe_-LjIg4el7YY6BpUtpRlk")
                    file.write(out_text)
                    print(out_text)
            except TimeoutError:
                print("error: server timed out")
