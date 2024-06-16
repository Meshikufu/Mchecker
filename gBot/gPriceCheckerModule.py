import time, requests, random, csv, os, time, win32gui, pywintypes
from bs4 import BeautifulSoup
from datetime import datetime
import json
import socket, socketio

from modules.SocketClient import Schat
from modules.SocketClientTTS import SchatTTS
import save.controlPanel
from modules.GoogleTTSv2 import TTSv2
from modules.Refresh_ControlPanel_json import Refresh_ControlPanel_json
import threading
from requests.exceptions import ConnectionError, Timeout, RequestException



#def jsonCP(variable):
#    with open('save/control_panel.json') as f:
#        json_control_panel = json.load(f)
#        return json_control_panel.get(variable)

PriceChecker_sleep_interrupt_thread = None


def date_Database():
    # Get the current date and time
    current_datetime = datetime.now()

    # Extract the year, month, day, and time
    current_year = current_datetime.year
    current_month = current_datetime.month
    current_day = current_datetime.day
    current_time = current_datetime.time()

    # Format the time as a string (HH:MM:SS)
    current_time_str = current_time.strftime('%H:%M:%S')

    # Store the data (date, time, and offer price) in the CSV file
    date_str = f"{current_day} - {current_month} - {current_year}"
    return date_str, current_time_str


def PriceMath(price, tts_ON, tts_NewPrice):
    from decimal import Decimal

    price = Decimal(str(price))  # Convert the price to a Decimal
    price_str = str(price)

    if '.' not in price_str:
        price_str += '.0'  # Append '.0' if there is no decimal part

    int_part, decimal_part = price_str.split('.')
    min_reduction = Decimal('1e-{0}'.format(len(decimal_part))) # Calculate the minimum reduction based on the length of the decimal part
    reduced_price = price - min_reduction # Calculate the reduced price
    
    # Check if the price is less than or equal to 3 and the decimal part has only one decimal place
    rand1 = str(random.randint(8, 9))
    rand2 = str(random.randint(97, 99))
    rand3 = str(random.randint(9, 9))
    if price <= 1 and len(decimal_part) == 1:
        decimal_part = str(int(decimal_part) - 1)
        reduced_price = float(f"{int_part}.{decimal_part}{rand2}")
    elif price <= 1 and len(decimal_part) == 2:
        decimal_part = str(int(decimal_part) - 1)
        reduced_price = float(f"{int_part}.{decimal_part}{rand1}")
    elif price <= 1 and len(decimal_part) == 3:
        decimal_part = str(int(decimal_part) - 1)
        reduced_price = float(f"{int_part}.{decimal_part}{rand1}")
    elif price <= 1 and len(decimal_part) > 3:
        reduced_price = str(reduced_price)
    elif price <= 2 and len(decimal_part) == 1:
        decimal_part = str(int(decimal_part) - 1)
        reduced_price = float(f"{int_part}.{decimal_part}{rand2}")
    elif price <= 2 and len(decimal_part) == 2:
        reduced_price = str(reduced_price)
    elif price <= 2 and len(decimal_part) >= 3:
        decimal_part = str(int(decimal_part) - 1)
        reduced_price = float(f"{int_part}.{decimal_part}{rand1}")
    elif price <= 3 and len(decimal_part) == 1:
        decimal_part = str(int(decimal_part) - 1)
        reduced_price = float(f"{int_part}.{decimal_part}{rand3}")
    elif price <= 3 and len(decimal_part) == 2:
        reduced_price = str(reduced_price)
    else:
        reduced_price = str(reduced_price)

    reduced_price = str(reduced_price)
    if '.' in reduced_price:
        print("if isinstance(reduced_price, float):")
        reduced_price_float = float(reduced_price)
        reduced_price_tts = round(reduced_price_float, 2)
        reduced_price_tts = str(reduced_price_tts).replace('.', ' ')
        print(reduced_price_tts)
        #ttsoff
        if tts_ON and tts_NewPrice:
            TTSv2(f"new price is:")
            TTSv2(f"{reduced_price_tts}")
        return reduced_price
    else:
        if tts_ON and tts_NewPrice:
            TTSv2(f"new price is:")
            TTSv2(f"{reduced_price}")
        return reduced_price

# Full path to the VirtualDesktopAccessor.dll file
import ctypes
VirtualDesktopAccessor_path = save.controlPanel.VirtualDesktopAccessor_path
vda = ctypes.WinDLL(VirtualDesktopAccessor_path)


def SeleniumChrome(new_decreased_price, CPJ):
    try:
        sleeptimer = 2
        #CPjson = Refresh_ControlPanel_json()
        CPjson = CPJ
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

            
        def remove_chrome_alert():
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
                            TTSv2(f"Error occurred while setting foreground window")
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

                desktop_check()

                
                # Clear the existing value and enter the new price
                input_field.clear()
                input_field.send_keys(str(new_decreased_price))

                # Locate and click the "Save" button
                save_button = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn--green.editable-submit'))
                )

                desktop_check()

                
                save_button.click()

            finally:
                driver.quit()
                print("done")
                if CPjson['tts_ON'] and CPjson['tts_Done']:
                    TTSv2("done")
                #time.sleep(4.5)
                remove_chrome_alert()
                #time.sleep(10)
    except Exception as e:
        print("An error occurred:", e)
        if CPjson['tts_ON'] and CPjson['tts_RetringIn60']:
            TTSv2("Retrying after 60 seconds...")
        winsound.Beep(1000, 500)
        winsound.Beep(1000, 500)
        winsound.Beep(1000, 500)
        pyautogui.hotkey('ctrl', 'win', 'right')
        pyautogui.hotkey('ctrl', 'r') 
        pyautogui.hotkey('ctrl', 'win', 'left')
        time.sleep(60)
        SeleniumChrome(new_decreased_price, CPJ)


def PriceChecker():
    
    testingPhase = save.controlPanel.testingPhase

    CPJ = Refresh_ControlPanel_json()
    testingPhase = CPJ['testingPhase']
    IterationSleepTime = CPJ['IterationSleepTime']

    print("gPriceChecker started")

    with open('save\control_panel.json') as f:
        json_control_panel = json.load(f)
        
        testingPhase = json_control_panel['testingPhase']


    if not os.path.exists("temp/interrupt_signal.txt"):
        with open("temp/interrupt_signal.txt", "w"):
            pass

    with open("temp/interrupt_signal.txt", "w") as clear_signal_file:
            clear_signal_file.write("prep")


    if testingPhase:
        testimeStart = save.controlPanel.testimeStart
        time.sleep(testimeStart)
    else:
        time.sleep(CPJ['PriceChecker_loop_start_time'])

    with open("temp/interrupt_signal.txt", "w") as clear_signal_file:
            clear_signal_file.write("")
    try:

        def process_sellerInfo(sellerInfo):
            date_str, current_time_str = date_Database()

            stock_str = sellerInfo.find('div', class_='offers-top-tittles', string='Stock').find_next('span').text.strip()
            stock_int = int(stock_str.replace(',', '').replace('Mil', ''))
            level_str = sellerInfo.find('div', class_='seller_level-peronal').text

            # new antibug int to float
            price_str = sellerInfo.find('span', class_='offer-price-amount').text.replace(',', '')
            if '.' not in price_str:
                price_str += '.0'  # Append '.0' if there is no decimal part
            price_float = float(price_str)

            seller_list = {
                'name': sellerInfo.find('div', class_='seller__name-detail').text,
                'level': int(level_str.replace('Level ', '')),
                'stock': min(stock_int, 999), # Cap stock at 999
                'price': min(price_float, 20),
                'time': current_time_str,
                'date': date_str
            }
            return seller_list
        
        dict_range = save.controlPanel.dict_range
        if testingPhase is True:
            dict_range = save.controlPanel.dict_rangeTest
        OldSeller = {}
        for i in dict_range:
            key = i
            OldSeller[key] = {}

        dict_filled = False
        skip = False
        skip_myname = False
        CurrentlySelling = False
        CurrentlySellingFlag = False
        CurrentlySellingOld = False
        CurrentlySellingTTS = False
        price_matched = False
        my_name = save.controlPanel.my_name
        target_name = save.controlPanel.target_name

        #interupt_sleep_priceChecker = threading.Event()


        # Event to signal the interrupt listener thread to stop
        interupt_sleep_priceChecker = threading.Event()
        stop_event = threading.Event()

        # Define the thread variable in a broader scope
        

        def listen_for_interrupt():
            if not os.path.exists("temp/interrupt_signal.txt"):
                with open("temp/interrupt_signal.txt", "w"):
                    pass
            while not stop_event.is_set():
                try:
                    with open("temp/interrupt_signal.txt", "r") as signal_file:
                        signal = signal_file.read().strip()
                        if signal == "interrupt":
                            print("Refresh SellerList")
                            interupt_sleep_priceChecker.set()
                            with open("temp/interrupt_signal.txt", "w") as clear_signal_file:
                                clear_signal_file.write("")
                    time.sleep(1) # without this it was easting 10% cpu WHAT
                except KeyboardInterrupt:
                    break

        def listen_and_run():
            listen_for_interrupt()

        def start_listen_for_interrupt():
            global PriceChecker_sleep_interrupt_thread
            if PriceChecker_sleep_interrupt_thread is not None:
                if PriceChecker_sleep_interrupt_thread.is_alive():
                    print("Stopping previous thread...")
                    stop_event.set()
                    PriceChecker_sleep_interrupt_thread.join()

            stop_event.clear()  # Clear the event for the next iteration

            PriceChecker_sleep_interrupt_thread = threading.Thread(target=listen_and_run, daemon=True)
            PriceChecker_sleep_interrupt_thread.start()


        def MSG_socketIO(msg):
            try:
                sio = socketio.Client()

                @sio.event
                def connect():
                    
                    print('Connection established')
                    send_message()

                @sio.event
                def disconnect():
                    print('Disconnected from server')

                @sio.on('message')
                def on_message(data):
                    print('Message from server:', data)

                @sio.on('response')
                def on_custom_response(data):
                    print('Custom response from server:', data['data'])

                def send_message():
                    sio.send(msg)


                ip_address = socket.gethostbyname(socket.gethostname())
                sio.connect(f'http://{ip_address}:8080')
            except Exception as e:
                print("MSG_socketIO has failed")
                print(e)


        while True:
            CPJ = Refresh_ControlPanel_json()
            testingPhase = CPJ['testingPhase']
            IterationSleepTime = CPJ['IterationSleepTime']

            
            with open("temp/interrupt_signal.txt", "w") as clear_signal_file:
                clear_signal_file.write("working")
            
            if testingPhase is False:
                url = save.controlPanel.gPriceCheckerURL_sellerList
                max_retries = 5
                backoff_factor = 1
                for attempt in range(max_retries):
                    try:        
                        response = requests.get(url)
                    except (ConnectionError, Timeout) as e:
                        print(f"Attempt {attempt + 1} failed: {e}")
                        time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff
                    except RequestException as e:
                        print(f"An error occurred: {e}")
                        time.sleep(2)
                        break
                html_content = response.text
            elif testingPhase is True:
                time.sleep(2)
                with open('gbot/Test_HTML.txt', 'r', encoding='utf-8') as html:
                    html_content = html.read()

            soup = BeautifulSoup(html_content, 'html.parser')

            pre_checkout_sls_offer_div = soup.find('div', {'id': 'pre_checkout_sls_offer', 'class': 'hide'})


            if pre_checkout_sls_offer_div is not None:
                other_seller_offer_mainboxes = pre_checkout_sls_offer_div.find_all('div', {'class': 'other-seller-offeer_mainbox'})
                other_seller_offer_mainboxes = other_seller_offer_mainboxes[0]


                seller1LowLevel = False
                CurrentlySellingFlag = False
                if CurrentlySelling is False and dict_filled is True:
                    CurrentlySellingTTS = True
                Seller = {}
                for i in dict_range:
                    n = 1
                    if seller1LowLevel is True:
                        i -= 1
                        n = 0
                    try:
                        Seller[i] = process_sellerInfo(other_seller_offer_mainboxes.find_all('div', {'class': 'other_offer-desk-main-box other_offer-div-box'})[i-n])
                        print(f"S[{i}]: {Seller[i]}")

                        if testingPhase is True:
                            testingPhase_first_sellers_price_change = save.controlPanel.testingPhase_first_sellers_price_change
                            if testingPhase_first_sellers_price_change is True:
                                if i == 1:
                                    Seller[i]['price'] = save.controlPanel.tsp1
                                elif i == 2:
                                    Seller[i]['price'] = save.controlPanel.tsp2
                                elif i == 3:
                                    Seller[i]['price'] = save.controlPanel.tsp3
                                elif i == 4:
                                    Seller[i]['price'] = save.controlPanel.tsp4
                                print("modded verison below")
                                print(f"S[{i}]: {Seller[i]}")
                            my_name_positon = save.controlPanel.my_name_positon
                            if i == my_name_positon:
                                Seller[i]['name'] = my_name
                                print("modded verison below")
                                print(f"S[{i}]: {Seller[i]}")

                        if CurrentlySellingFlag is False:
                            if Seller[i]['name'] == my_name:
                                CurrentlySelling = True
                                CurrentlySellingFlag = True
                                if CurrentlySellingTTS is True:
                                    CurrentlySellingTTS = False
                                    TTSv2("Back online!")
                            else:
                                CurrentlySellingFlag = False
                                CurrentlySelling = False

                        if seller1LowLevel is False:
                            if Seller[1]['level'] < 5 :
                                seller1LowLevel = True
                                #Schat("changing sellers low level structure because of low level seller")
                                #Schat("changing sellers low level structure because of low level seller")
                                print("changing sellers low level structure because of low level seller")

                            elif Seller[1]['stock'] <= 15 and Seller[1]['price'] < 1:
                                seller1LowLevel = True
                                #Schat("changing sellers low level structure because of low level seller")
                                #Schat("changing sellers low level structure because of low level seller")
                                print("changing sellers low level structure because of low stock seller")
                        else:
                            seller1LowLevel == True
                        
                        OutOfRangePosition = i

                    except IndexError:
                        # Handle the case where the index is out of range
                        print(f"Seller in position {i} doesn't exist.")
                        print(f"Seller number: {i-1}")
                        OutOfRangePosition = i
                        break
                

                #if CurrentlySellingFlag is False:



            #here!
            
            def packSellerInfo():
                seller_data = []

                try:
                    for i in range(1, 11):
                        seller_data.append(Seller[i])
                except IndexError:
                    pass

                wrapped_data = {"SellerList": seller_data}
                json_data = json.dumps(wrapped_data)

                MSG_socketIO(json_data)

            if CPJ['msgClientWebpage'] is True:
                packSellerInfo()



            if dict_filled and CurrentlySelling is False and CurrentlySellingOld is True:
                TTSv2("Offline!")  
            elif pre_checkout_sls_offer_div is None:
                TTSv2("Price Checker items are none")


            # Print the results
            print("Time:", Seller[1]['time'])
            print("Date:", Seller[1]['date'])

            current_datetime = datetime.now()
            current_year = current_datetime.year
            current_month = current_datetime.month
            current_day = current_datetime.day

            LowestPrice = {}
            LowestPrice[OutOfRangePosition] = Seller[1].copy()
            LowestPrice[OutOfRangePosition]['name'] = '$LowestPrice$'
            # Join the folder name and file name to create the complete file path
            folder_name = r"C:\Users\Kufu\PythonProjects\Mchecker\gBot"
            #folder_name = "gBot"
            file_path = os.path.join(folder_name, f'Gdata{current_year}.csv')
            
            # Write data to the CSV file
            with open(file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for i in dict_range:
                    try:
                        writer.writerow([Seller[i]['date'], Seller[i]['time'], Seller[i]['price'], Seller[i]['name'], Seller[i]['stock'], Seller[i]['level']])
                    except KeyError:
                        # Write lowest price when loop reaches not existent seller
                        writer.writerow([LowestPrice[i]['date'], LowestPrice[i]['time'], LowestPrice[i]['price'], LowestPrice[i]['name'], LowestPrice[i]['stock'], LowestPrice[i]['level']])
                        break


            NewName = Seller[1]['name']
            NewPrice = Seller[1]['price']
            NewStock = Seller[1]['stock']


            if testingPhase is True:
                import copy

                CurrentlySelling = True

                for i in dict_range:
                    try:
                        OldSeller[i] = copy.deepcopy(Seller[i])
                    except KeyError:
                        break

                OldName = NewName
                OldPrice = NewPrice
                OldStock = NewStock
                dict_filled = True

                print(Seller[1])
                print(OldSeller[1])

                Seller[1]['name'] = "Testing"

                print(Seller[1])
                print(OldSeller[1])

                #Seller[1]['price'] -= 0.0003
                TestNewPrice = save.controlPanel.TestNewPrice
                Seller[1]['price'] = TestNewPrice
                #OldSeller[1]['price'] = 1.2

                NewName = Seller[1]['name']
                NewPrice = Seller[1]['price']
                NewStock = Seller[1]['stock']

                print("testing name and price swap")
                print(Seller[1])
                print(OldSeller[1])


            print(f"current selling is: {CurrentlySelling}")
            if CurrentlySelling is True:

                if Seller[1]['name'] != my_name and dict_filled is True:

                    print("first pass")
                    print(Seller[1]['name'])
                    print(OldSeller[1]['name'])
                    # checking if seller with lowest price is still with lowest price
                    if Seller[1]['name'] != OldSeller[1]['name'] or Seller[1]['price'] != OldSeller[1]['price'] or Seller[1]['stock'] != OldSeller[1]['stock'] or testingPhase is True:
                        skip = False
                        skip_myname = False
                        new_account_skip = False
                        print(skip)
                        print(f"OldSeller[1]['price']: {OldSeller[1]['price']}")
                        print(f"Seller[1]['price']: {Seller[1]['price']}")
                        print(f"OldSeller[1]['stock']: {OldSeller[1]['stock']}")
                        print(f"Seller[1]['stock']: {Seller[1]['stock']}")


                        ### check for new account
                        if Seller[1]['level'] < 5:
                            skip = True
                            new_account_skip = True


                        ### price change 
                        if OldPrice > NewPrice and new_account_skip is False:
                            final_price = OldPrice - NewPrice
                            print(f"final price is: {final_price}, old price is: {OldPrice}, price: {NewPrice}")
                            if final_price < 1:
                                final_price_int = int(final_price * 100)
                                if final_price < 0.01:
                                    message = (f"{Seller[1]['name']} stole position")
                                    #Schat(message)
                                    #print(f"### price change  message is: {message}")
                                    skip = True
                                elif final_price < 0.99 and final_price > 0.01:
                                    if final_price_int == 1:
                                        message = f"{Seller[1]['name']} lowered price by {final_price_int} cent"
                                    elif final_price <= 0.99:
                                        message = f"{Seller[1]['name']} lowered price by {final_price_int} cents"
                                    #print(message)
                            else:
                                message = f"{Seller[1]['name']} lowered price by {final_price:.2f} Euro"
                            
                            #ttsoff
                            if CPJ['tts_ON'] and CPJ['tts_NewSeller']:
                                TTSv2(message)

                            ### main price change fucntion
                            from decimal import Decimal
                            def reduce_price(price):
                                print("### Price is below ###")
                                print(price)
                                price = Decimal(str(price))  # Convert the price to a Decimal

                                price_str = str(price)
                                int_part, decimal_part = price_str.split('.')

                                # Calculate the minimum reduction based on the length of the decimal part
                                min_reduction = Decimal('1e-{0}'.format(len(decimal_part)))
                                
                                # Calculate the reduced price
                                reduced_price = price - min_reduction
                                
                                # Check if the price is less than or equal to 3 and the decimal part has only one decimal place
                                rand1 = str(random.randint(8, 9))
                                rand2 = str(random.randint(97, 99))
                                rand3 = str(random.randint(9, 9))
                                if price <= 2 and len(decimal_part) == 1:
                                    decimal_part = str(int(decimal_part) - 1)
                                    reduced_price = float(f"{int_part}.{decimal_part}{rand2}")
                                elif price <= 2 and len(decimal_part) == 2:
                                    decimal_part = str(int(decimal_part) - 1)
                                    reduced_price = float(f"{int_part}.{decimal_part}{rand1}")

                                elif price <= 3 and len(decimal_part) == 1:
                                    decimal_part = str(int(decimal_part) - 1)
                                    reduced_price = float(f"{int_part}.{decimal_part}{rand1}")
                                elif price <= 3 and len(decimal_part) == 2:
                                    decimal_part = str(int(decimal_part) - 1)
                                    reduced_price = float(f"{int_part}.{decimal_part}{rand1}")
                                else:
                                    decimal_part = str(int(decimal_part) - 1)
                                    reduced_price = float(f"{int_part}.{decimal_part}{rand3}")
                                    #reduced_price = str(reduced_price)
                                
                                
                                return reduced_price

                            new_decreased_price = PriceMath(NewPrice, CPJ.get('tts_ON'), CPJ.get('tts_NewPrice'))
                            import pyperclip
                            pyperclip.copy(str(new_decreased_price))
                            Schat(f"New price is {new_decreased_price}")


                            medianPrice = (Seller[2]['price'] + Seller[3]['price'] + Seller[4]['price']) / 3
                            priceDiff = abs(medianPrice - Seller[1]['price'])
                            thresholdPercentage = 0.03
                            if NewPrice > 6:
                                thresholdPercentage = 0.3
                            elif NewPrice > 4:
                                thresholdPercentage = 0.15
                            if testingPhase:
                                thresholdPercentage = 0.4
                            print(f"median price of Seller[2-4] is: {medianPrice}")
                            print(f"price diff is: {priceDiff}")

                            if priceDiff <= thresholdPercentage or Seller[1]['price'] == Seller[3]['price']:
                                if CPJ['tts_ON'] and CPJ['tts_ChangingPrice']:
                                    TTSv2(f"changing price")
                                    TTSv2(f"{new_decreased_price}")
                                Schat(f"changing price")
                                Schat(f"Time: {Seller[1]['time']}")
                            

                                SeleniumChrome(new_decreased_price, CPJ)

                                
                            elif priceDiff > thresholdPercentage:
                                if CPJ['tts_ON'] and CPJ['tts_ChangeManually']:
                                    TTSv2(f"change price manually")
                                Schat(f"change price manually")
                                Schat(f"Time: {Seller[1]['time']}")
                                price_matched = False

                        ### new seller matched price, and he is now above in the list
                        #elif Seller[1]['name'] == my_name or Seller[2]['name'] == my_name and price_matched is False and Seller[1]['price'] == Seller[2]['price']:
                        elif Seller[2]['name'] == my_name or Seller[3]['name'] == my_name and price_matched is False and Seller[1]['price'] == Seller[2]['price']:
                            if Seller[1]['name'] != OldSeller[1]['name'] or Seller[2]['name'] != OldSeller[2]['name']:
                                if Seller[1]['price'] == Seller[2]['price']:
                                    if CPJ['tts_ON'] and CPJ['tts_Matched']:
                                        TTSv2(f"Matched!")
                                    print(f"price matched!")

                                    
                                    price_matched = True
                                    matchSellers = save.controlPanel.matchSellers
                                    
                                    new_decreased_price = PriceMath(NewPrice)

                                    if matchSellers == False:
                                        SeleniumChrome(new_decreased_price)

                                    Schat(f"Price to copy: {new_decreased_price}")
                                    import pyperclip
                                    pyperclip.copy(str(new_decreased_price))


                        ### some one got offline or sold everything or changed price to higher
                        elif OldPrice < NewPrice and new_account_skip is False:
                            final_price = NewPrice - OldPrice
                            final_price_int = int(final_price * 100)
                            if final_price < 0.01:
                                message = f"price slightly got higher"
                            elif final_price < 1 and final_price > 0.01:
                                message = f"price got higher by {final_price_int} cents"
                            elif final_price_int == 1:
                                message = f"price got higher by {final_price_int} cent"
                            else:
                                message = f"price got higher by {final_price:.2f} Euro"
                            if CPJ['tts_ON'] and CPJ['tts_SlightyHigher']:
                                TTSv2(message)
                            print(f"### price change  message is: {message}")

                        ### part of stock sold
                        elif OldPrice == NewPrice:
                            if skip is False:
                                if NewName == OldName and NewPrice == OldPrice and NewStock < OldStock:
                                    message = f"{NewName} sold {OldStock - NewStock} divines"
                                    if CPJ['tts_ON'] and CPJ['tts_SoldStock']:
                                        TTSv2(message)
                                    print(message)
                                    skip = True
                        else:
                            if new_account_skip is False:
                                message = f"{Seller[1]['name']} just matched price"
                                print(message)
                                #Schat(message)
                                skip = True


                        ### if first position seller sold all his stock
                        if skip is False and new_account_skip is False:
                            if Seller[1]['name'] == OldSeller[2]['name'] and Seller[1]['stock'] == OldSeller[2]['stock'] and Seller[1]['price'] == OldSeller[2]['price']:
                                message = f"{OldSeller[1]['name']} sold all {OldSeller[1]['stock']} divines"
                                message = f"pos 1 sold everything or went offline"
                                #Schat(message)
                                print(f"### if first position seller sold all his stock message is: {message}")
                                skip = True


                        ### stock block
                        if skip is False and new_account_skip is False:
                            if int(Seller[1]['stock']) <= 5:
                                message = f"small amount"
                                #Schat(message)
                                print(f"### stock block message is: {message}")
                            elif int(Seller[1]['stock']) > 80:
                                message = f"large quantity"
                                #Schat(message)
                                print(f"### stock block message is: {message}")
                            elif int(Seller[1]['stock']) >= 30:
                                message = f"big stock"
                                #Schat(message)
                                print(f"### stock block message is: {message}")
                        

                        ### my name check block if price was changed
                        if skip is False and new_account_skip is False:
                            for i in range(2, 5):
                                #current_seller = locals().get(f"seller{i}")
                                #current_seller = Seller[i]
                                if Seller[i]['name'] == my_name:
                                    #price = float(current_seller['price'])
                                    #price = Seller[i]['price']
                                    #price1 = Seller[1]['price']
                                    final_price = Seller[i]['price'] - Seller[1]['price']
                                    if final_price < 1 and final_price > 0.01:
                                        final_price_int = int(final_price * 100)
                                        message = f"Price difference is {final_price_int} cents"
                                    elif final_price <= 0.01:
                                        message = f"slight price difference"
                                    elif final_price == 0.01:
                                        final_price_int = int(final_price * 100)
                                        message = f"Price difference is {final_price_int} cent"
                                    else:
                                        message = f"Price difference is {final_price:.2f} Euro"
                                    #Schat(message)
                                    print(f"### my name check block message is: {message}")
                                    skip_myname = True


                        ### im not in the list 
                        if skip_myname is False:
                            if my_name != Seller[1]['name'] and my_name != Seller[2]['name'] and my_name != Seller[3]['name'] and my_name != Seller[4]['name']:
                                message = 'You are not in the list!'
                                #Schat(message)
                                print(message)

                    else:
                        print("Nothing has changed")
                        
                elif Seller[1]['name'] == my_name:
                    print(f"{Seller[1]['name']} has the lowest price")


                    if dict_filled is True and Seller[2]['price'] > OldSeller[2]['price'] and my_name == Seller[1]['name'] and Seller[1]['price'] == OldSeller[1]['price']:
                        result =  OldSeller[2]['price'] - Seller[1]['price']
                        if result > 0.02:
                            positionTwoPriceDifference = OldSeller[2]['price'] - Seller[1]['price']
                            if CPJ['tts_ON'] and CPJ['tts_Pos2GotHigher']:
                                TTSv2(f"position 2 price got higher. Difference {positionTwoPriceDifference:.2f}")

                            NewPrice = Seller[2]['price']
                            decimal_value = NewPrice
                            decimal_str = str(decimal_value)
                            whole_part, decimal_part = decimal_str.split('.')
                            new_decimal_part = str(int(decimal_part) - 1)
                            new_decimal_str = whole_part + '.' + new_decimal_part
                            new_decreased_price = float(new_decimal_str)

                            if CPJ['tts_ON'] and CPJ['tts_Pos2LoweredPrice']:    
                                TTSv2(f"New pos2 lowered price to copy: {new_decreased_price}")
                            import pyperclip
                            pyperclip.copy(str(new_decreased_price))

                            # todo automate

                    target_tracking = save.controlPanel.target_tracking
                    if target_tracking is True:
                        target_name_trigger  = 0
                        target_name_trigger_cell1 = False
                        target_name_trigger_cell2 = False

                        if dict_filled is True:
                            for i in dict_range:
                                if target_name_trigger_cell1 is False:
                                    try:
                                        if Seller[i]['name'] == target_name:
                                            target_price_new = Seller[i]['price']
                                            target_name_trigger += 1
                                            target_name_trigger_cell1 = True
                                            print(f"{target_name} test cell 1: {target_price_new} and {Seller[i]['price']}")
                                    except KeyError:
                                        print(f"Error: cell 1 Seller in position {i} doesn't exist.")
                                        break
                                if target_name_trigger_cell2 is False:
                                    try:
                                        if OldSeller[i]['name'] == target_name:
                                            target_price_old = OldSeller[i]['price']
                                            target_name_trigger += 1
                                            target_name_trigger_cell2 = True
                                            print(f"{target_name} test cell 2: {target_price_old} and {OldSeller[i]['price']}")
                                    except KeyError:
                                        print(f"Error: cell 2 Seller in position {i} doesn't exist.")
                                        break
                                if target_name_trigger == 2:
                                    if target_price_new > target_price_old:
                                        message = f"{target_name} raised price"
                                        print(message)
                                        if CPJ['tts_ON'] and CPJ['tts_RaisedPrice']:
                                            TTSv2(message)
                                        break
                                    elif target_price_new < target_price_old:
                                        message = f"{target_name} lowered price"
                                        print(message)
                                        if CPJ['tts_ON'] and CPJ['tts_LoweredPrice']:
                                            TTSv2(message)
                                        break
                                    else:
                                        print(f"{target_name} has same price")
                                        break
                                else:
                                    continue

                

                print(f"skip: {skip}")

            ### Make current iteration as Old dictionary for sellers
            for i in dict_range:
                try:
                    OldSeller[i] = Seller[i]
                    #print(OldSeller[i])
                except KeyError:
                    #print(f"Error: Seller in position {i} doesn't exist.")
                    break
            

            OldName = NewName
            OldPrice = NewPrice
            OldStock = NewStock

            print("")
            dict_filled = True


            

            #print("iteration time")
            #print(IterationSleepTime)
            fluctuation_percentage = random.uniform(-0.05, 0.05)
            IterationSleepTime = IterationSleepTime * (1 + fluctuation_percentage)
            if testingPhase is True:
                IterationSleepTime = save.controlPanel.TEST_IterationSleepTime
            #print("iteration time")
            #print(IterationSleepTime)
            #IterationSleepTime = 1000

            def print_active_threads():
                # Get a list of all active threads
                active_threads = threading.enumerate()
                
                # Print information about each thread
                print(f"Total active threads: {len(active_threads)}\n")
                for thread in active_threads:
                    print(f"Thread Name: {thread.name}")
                    print(f"Thread ID: {thread.ident}")
                    print(f"Is Alive: {thread.is_alive()}")
                    print(f"Daemon: {thread.daemon}\n")
            
            #print_active_threads()

            print(IterationSleepTime)
            with open("temp/interrupt_signal.txt", "w") as clear_signal_file:
                clear_signal_file.write("sleep")
            start_listen_for_interrupt()            
            interrupted_priceChecker = interupt_sleep_priceChecker.wait(timeout=IterationSleepTime)
            if interrupted_priceChecker:
                interupt_sleep_priceChecker.clear()
            #time.sleep(IterationSleepTime)
            
            # interupt_sleep_priceChecker.set() to interupt sleep
    except Exception as e:
        import traceback
        traceback.print_exc()  # Print the traceback to see the error details
        TTSv2("Error in Price checker!")
        input("PriceChecker got An error. Press Enter to exit...")