# create by github.com/niizam , edit by YarBurArt
from playwright.sync_api import Playwright, sync_playwright, expect
from playwright._impl._api_types import TimeoutError


def run(playwright, message):
    # chara_id = "zb7I4U9OYfewmEgOWLBHScefPeELkm1J-_GZDjHLY1M" # q&a
    chara_id = "3LnH7nShX-dOrtOpJ0MSBgkuuA2PFjZI4nSiJ997iSc"  # rei 1
    context = playwright.firefox.launch(headless=True).new_context()
    page = context.new_page()
    page.goto('https://beta.character.ai/chat?char=' + chara_id)

    page.get_by_role("button", name="Accept").click()
    page.get_by_placeholder("Type a message").fill(message)
    page.get_by_placeholder("Type a message").press("Enter")

    page.wait_for_selector('.swiper-button-next').is_visible()
    div = page.query_selector('div.msg.char-msg')
    output_text = div.inner_text()

    context.close()
    return output_text


if __name__ == '__main__':
    message = input(">>> ")
    try:
        with sync_playwright() as playwright:
            print(run(playwright, message))
    except TimeoutError:
        print("error")
