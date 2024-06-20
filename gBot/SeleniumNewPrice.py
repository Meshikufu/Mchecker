import ctypes, win32gui, pywintypes
import time
import save.controlPanel
from modules.GoogleTTSv2 import TTSv2
#from modules.Refresh_ControlPanel_json import Refresh_ControlPanel_json
change_price1 = save.controlPanel.change_price1
change_price2 = save.controlPanel.change_price2
change_price3 = save.controlPanel.change_price3
change_to_online1 = save.controlPanel.change_to_online1
change_to_online2 = save.controlPanel.change_to_online2
change_to_offline1 = save.controlPanel.change_to_offline1
change_to_offline2 = save.controlPanel.change_to_offline2


VirtualDesktopAccessor_path = save.controlPanel.VirtualDesktopAccessor_path
vda = ctypes.WinDLL(VirtualDesktopAccessor_path)



def SeleniumChrome(new_decreased_price, CPJ, option):
    try:
        errorCondition = False
        change_price = False
        change_to_online = False
        change_to_offline = False

        if option == 'change_price':
            change_price = True
        elif option == 'change_to_online':
            change_to_online = True
        elif option == 'change_to_offline':
            change_to_offline = True

        with open("temp/interrupt_signal.txt", "w") as clear_signal_file:
            clear_signal_file.write("working")

        sleeptimer = 2
        CPjson = CPJ
        CPjson['autoChangePrice'] = True
        
        if CPjson['tts_ON'] and CPjson['tts_ChangingPriceIN']:
            TTSv2(f"changing price in {2}")
        time.sleep(sleeptimer)

        import winsound
        import pyautogui
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
                pyautogui.hotkey('ctrl', 'r') 
                pyautogui.hotkey('ctrl', 'win', 'left')
                print("returning to desktop 0")

            
        def remove_chrome_alert(errorCondition):
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
                    retry_count = 10
                    while retry_count > 0:
                        if retry_count <= 2:
                            time.sleep(0.5)
                        try:
                            win32gui.SetForegroundWindow(chrome_handle)
                            win32gui.FlashWindow(chrome_handle, False)  # This example is for illustration, may not directly work with browser tabs.
                            break
                        except pywintypes.error as e:
                            print(f"Error occurred while setting foreground window: {e}")
                            #TTSv2(f"Error occurred while setting foreground window")
                            retry_count -= 1
                            if retry_count > 0:
                                print(f"Retrying... {retry_count} attempts left.")
                                time.sleep(1)
                    if retry_count == 0:
                        print("Failed to set foreground window after retries.")
                else:
                    print("Chrome window not found.")


            window_title = save.controlPanel.window_title
            remove_flashing_state(window_title)

            # Continuously monitor desktopNum and execute pyautogui.hotkey('ctrl', 'win', 'left') when desktopNum is 1
            sleepReruns = 0
            while True:
                desktopNum = get_current_desktop_number()
                if desktopNum == 1:
                    if errorCondition:
                        pyautogui.hotkey('ctrl', 'r') 
                    pyautogui.hotkey('ctrl', 'win', 'left')
                    print(sleepReruns)
                    break
                time.sleep(0.004)
                sleepReruns = sleepReruns + 1
                print(sleepReruns)


        if CPjson['autoChangePrice']:

            myPage = save.controlPanel.gPriceCheckerURL_myPage

            # Switch to Desktop 2 (assuming you have Desktop 2)
            desktop_name = "Desktop 2"
            switch_to_desktop(desktop_name)

            # Set up Chrome options for connecting to an existing instance
            chrome_options = Options()
            chrome_options.debugger_address = "127.0.0.1:9227"  # Use the correct address and port
            # Run Chrome in headless mode to hide the browser window
            chrome_options.add_argument("--headless")
            # Initialize the ChromeDriver with the specified options
            driver = webdriver.Chrome(options=chrome_options)
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
                    driver.get(myPage)


                # first step
                if change_price:
                    locator = (By.CLASS_NAME, change_price1)
                elif change_to_online:
                    locator = (By.XPATH, change_to_online1)
                elif change_to_offline:
                    locator = (By.XPATH, change_to_offline1)
                if change_price or change_to_online or change_to_offline:
                    element = WebDriverWait(driver, 1).until(EC.presence_of_element_located(locator))
                    desktop_check()
                    element.click()

                if change_price:
                    locator = (By.CSS_SELECTOR, change_price2)
                if change_price:
                    # Locate the input field for the price
                    input_field = WebDriverWait(driver, 2).until(EC.visibility_of_element_located(locator))
                    desktop_check()
                    # Clear the existing value and enter the new price
                    input_field.clear()
                    input_field.send_keys(str(new_decreased_price))

                # last step
                if change_price:
                    locator = (By.CSS_SELECTOR, change_price3)
                elif change_to_online:
                    locator = (By.XPATH, change_to_online2)
                elif change_to_offline:
                    locator = (By.XPATH, change_to_offline2)
                if change_price or change_to_online or change_to_offline:
                    final_confirm_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located(locator))
                    desktop_check()
                    final_confirm_button.click()

            finally:
                driver.quit()
                #time.sleep(4.5)
                remove_chrome_alert(errorCondition)
                if CPjson['tts_ON'] and CPjson['tts_Done']:
                    TTSv2("done")
                print("done")

                with open("temp/interrupt_signal.txt", "w") as clear_signal_file:
                    clear_signal_file.write("sleep")
                #TTSv2("done")
                #time.sleep(10)
    except Exception as e:
        errorCondition = True
        print("An error occurred:", e)
        if CPjson['tts_ON'] and CPjson['tts_RetringIn60']:
            TTSv2("Retrying after 60 seconds...")
        time.sleep(5)
        winsound.Beep(1000, 500)
        winsound.Beep(1000, 500)
        winsound.Beep(1000, 500)
        #pyautogui.hotkey('ctrl', 'win', 'right')
        #pyautogui.hotkey('ctrl', 'r') 
        #pyautogui.hotkey('ctrl', 'win', 'left')
        remove_chrome_alert(errorCondition)
        time.sleep(60)
        SeleniumChrome(new_decreased_price, CPJ)


#new_price = 5
#wan = Refresh_ControlPanel_json()
#SeleniumChrome(new_price, wan, 'change_to_online')