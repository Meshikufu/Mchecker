import time
import save.controlPanel
import ctypes
import pyautogui
import pywintypes
import win32gui

VirtualDesktopAccessor_path = save.controlPanel.VirtualDesktopAccessor_path
vda = ctypes.WinDLL(VirtualDesktopAccessor_path)

def SeleniumChrome(new_decreased_price):
    try:
        print("starting2")
        import winsound
        import pygetwindow as gw
        from selenium import webdriver
        from selenium.webdriver.common.by import By

        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.common.exceptions import TimeoutException
        
        from selenium.webdriver.chrome.options import Options


        def switch_to_desktop(desktop_name):
            desktop = gw.getWindowsWithTitle(desktop_name)
            if desktop:
                desktop[0].activate()

        def desktop_check():
            num = vda.GetCurrentDesktopNumber()
            print(num)
            if num == 1:
                #pyautogui.hotkey('ctrl', 'win', 'right')
            #    pyautogui.hotkey('ctrl', 'r') 
            #    pyautogui.hotkey('ctrl', 'win', 'left')
                print("returning to desktop 0")
              
            
        def remove_chrome_alert():
            print("removeAlert")
        #    winsound.Beep(1000, 500)
        #    winsound.Beep(1000, 500)
        #    time.sleep(0.5)
        #    pyautogui.hotkey('ctrl', 'win', 'right')
        #    pyautogui.press('pageup')
        #    pyautogui.hotkey('ctrl', 'win', 'left') 

        # Switch to Desktop 2 (assuming you have Desktop 2)
        myPage = save.controlPanel.gPriceCheckerURL_myPage
        desktop_name = "Desktop 2"
        switch_to_desktop(desktop_name)

        # Set up Chrome options for connecting to an existing instance
        chrome_options = Options()
        chrome_options.debugger_address = "127.0.0.1:9227"  # Use the correct address and port
        chrome_options.add_argument("--headless")
        
        print('start')
        driver = webdriver.Chrome(options=chrome_options)
        print('end')

        #chromedriverPathBeta = save.controlPanel.chromedriverPathBeta
        #driver = webdriver.Chrome(executable_path=chromedriverPathBeta, options=chrome_options)
        
        try:



            m1 = 1
            if m1 == 1:
                # Get the current window handle
                original_window_handle = driver.current_window_handle

                # Open the G2G URL in a new tab (can be the current tab)
                driver.execute_script("window.open('" + myPage + "', '_blank');")

                # Switch back to the original tab
                driver.switch_to.window(original_window_handle)
            if m1 == 2:
                # Navigate to the web page
                driver.get(myPage)  # Replace with the URL of the webpage you want to edit



            # Wait for the price element to be present on the page
            element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'g2g_products_price'))
            )
            desktop_check()


            element.click()

            # Locate the input field for the price
            input_field = WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.input-large'))
            )

            num = desktop_check()
            if num == 1:
                return num
            
            # Clear the existing value and enter the new price
            input_field.clear()
            input_field.send_keys(str(new_decreased_price))

            # Locate and click the "Save" button
            save_button = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn--green.editable-submit'))
            )

            num = desktop_check()
            if num == 1:
                return num
            
            save_button.click()

        finally:
            print("DONE")
            driver.quit()

    except Exception as e:
        print("An error occurred:", e)
        winsound.Beep(1000, 500)
        winsound.Beep(1000, 500)
        winsound.Beep(1000, 500)
        pyautogui.hotkey('ctrl', 'win', 'right')
        pyautogui.hotkey('ctrl', 'r') 
        pyautogui.hotkey('ctrl', 'win', 'left')
        time.sleep(60)
        SeleniumChrome(new_decreased_price)





def chromeNotificationRemover():
    # Load VirtualDesktopAccessor.dll

    def get_current_desktop_number():
        # Call GetCurrentDesktopNumber from VirtualDesktopAccessor.dll
        return vda.GetCurrentDesktopNumber()

    def find_chrome_window(window_title):
        chrome_handle = None
        top_windows = []
        win32gui.EnumWindows(lambda hwnd, top_windows: top_windows.append((hwnd, win32gui.GetWindowText(hwnd))), top_windows)
        for hwnd, window_text in top_windows:
            if window_title in window_text:
                chrome_handle = hwnd
                break
        return chrome_handle

    def remove_flashing_state(window_title):
        chrome_handle = find_chrome_window(window_title)
        if chrome_handle:
            retry_count = 3  # Number of times to retry setting foreground
            while retry_count > 0:
                if retry_count <= 2:
                    time.sleep(0.5)
                try:
                    # Attempt to bring the window to the foreground
                    win32gui.SetForegroundWindow(chrome_handle)
                    #time.sleep(0.5)  # Small delay to allow window to come to the foreground

                    # Optional: If you know how to send specific messages to Chrome windows, you could attempt to clear the flashing state here.
                    # However, manipulating browser tabs' internal states like flashing usually requires browser-level APIs.

                    # Example of how to remove flashing state using win32gui:
                    win32gui.FlashWindow(chrome_handle, False)  # This example is for illustration, may not directly work with browser tabs.

                    break  # Exit loop if successful

                except pywintypes.error as e:
                    print(f"Error occurred while setting foreground window: {e}")
                    retry_count -= 1
                    if retry_count > 0:
                        print(f"Retrying... {retry_count} attempts left.")
                        time.sleep(1)  # Wait before retrying

            if retry_count == 0:
                print("Failed to set foreground window after retries.")
        else:
            print("Chrome window not found.")


    # Usage example:
    window_title = "Free Listing & access to millions of Users Globally - Google Chrome"
    remove_flashing_state(window_title)

    # Continuously monitor desktopNum and execute pyautogui.hotkey('ctrl', 'win', 'left') when desktopNum is 1
    sleepReruns = 0
    while True:
        desktopNum = get_current_desktop_number()
        if desktopNum == 1:
            pyautogui.hotkey('ctrl', 'win', 'left')
            print(sleepReruns)
            break
        time.sleep(0.004)  # Adjust the sleep duration as needed to balance performance and responsiveness
        sleepReruns = sleepReruns + 1
        print(sleepReruns)


def times():
    SeleniumChrome(1.23)
    chromeNotificationRemover()

#times()
x = 0
while True:
    times()
    x = x + 1
    print(x)