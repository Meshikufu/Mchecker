import time, requests, random, csv, os
from bs4 import BeautifulSoup
from datetime import datetime

from modules.SocketClient import Schat
import save.controlPanel

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

#    # Print the results
#    print("Time:", current_time_str)
#    print("Date:", current_day, "-", current_month, "-", current_year)
#
    # Store the data (date, time, and offer price) in the CSV file
    date_str = f"{current_day} - {current_month} - {current_year}"
    return date_str, current_time_str



def PriceChecker():
    print("gPriceChecker started")
    testingPhase = save.controlPanel.testingPhase

    if testingPhase:
        time.sleep(5)
    else:
        time.sleep(5*12)
    try:

        def process_sellerInfo(sellerInfo):
            date_str, current_time_str = date_Database()

            stock_str = sellerInfo.find('div', class_='offers-top-tittles', string='Stock').find_next('span').text.strip()
            stock_int = int(stock_str.replace(',', '').replace('Mil', ''))
            level_str = sellerInfo.find('div', class_='seller_level-peronal').text
            price_float = float(sellerInfo.find('span', class_='offer-price-amount').text)
            seller_list = {
                'name': sellerInfo.find('div', class_='seller__name-detail').text,
                'level': int(level_str.replace('Level ', '')),
                #'delivery_method': sellerInfo.find('div', class_='offers-top-tittles', string='Delivery method').find_next('div', class_='tippy').text.strip(),
                #'delivery_speed': sellerInfo.find('div', class_='offers-top-tittles', string=' Delivery speed').find_next('span').text.strip(),
                'stock': min(stock_int, 999), # Cap stock at 999
                #'stock': int(stock_str.replace(',', '').replace('Mil', '')),
                #'min_purchase': sellerInfo.find('div', class_='offers-top-tittles', string='Min. purchase').find_next('span').text.strip(),
                'price': min(price_float, 15),
                #'currency_unit': sellerInfo.find('span', class_='offers_amount-currency-regional').text
                'time': current_time_str,
                'date': date_str
            }
            return seller_list
        
        dict_range = save.controlPanel.dict_range
        OldSeller = {}
        for i in dict_range:
            key = i
            OldSeller[key] = {}

        dict_filled = False
        skip = False
        skip_myname = False
        CurrentlySelling = False
        CurrentlySellingOld = False
        price_matched = False
        my_name = save.controlPanel.my_name
        target_name = save.controlPanel.target_name
        TestMethodSelenium = save.controlPanel.TestMethodSelenium

        
        

        ### TEST SWITCH
        test_phase = save.controlPanel.test_phase
        test_number = 1

        while True:

            if test_phase is False:
                url = save.controlPanel.gPriceCheckerURL_sellerList
                response = requests.get(url)
                html_content = response.text

                soup = BeautifulSoup(html_content, 'html.parser')

                pre_checkout_sls_offer_div = soup.find('div', {'id': 'pre_checkout_sls_offer', 'class': 'hide'})


                if pre_checkout_sls_offer_div is not None:
                #    if pre_checkout_sls_offer_div is not None:
                #        other_seller_offer_mainboxes = pre_checkout_sls_offer_div.find_all('div', {'class': 'other-seller-offeer_mainbox'})
                #        
                #        if other_seller_offer_mainboxes:
                #            # Your code to process the 'other_seller_offer_mainboxes' here
                #        else:
                #            print("No 'other-seller-offeer_mainbox' elements found.")
                #    else:
                #        print("No 'pre_checkout_sls_offer' div found.")


                    other_seller_offer_mainboxes = pre_checkout_sls_offer_div.find_all('div', {'class': 'other-seller-offeer_mainbox'})
                    other_seller_offer_mainboxes = other_seller_offer_mainboxes[0]


                    seller1LowLevel = False
                    Seller = {}
                    for i in dict_range:
                        n = 1
                        if seller1LowLevel is True:
                            i -= 1
                            n = 0
                        try:
                            Seller[i] = process_sellerInfo(other_seller_offer_mainboxes.find_all('div', {'class': 'other_offer-desk-main-box other_offer-div-box'})[i-n])
                            print(f"S[{i}]: {Seller[i]}")
                            if seller1LowLevel is False:
                                if Seller[1]['level'] < 5 :
                                    seller1LowLevel = True
                                    #Schat("$tts changing sellers low level structure because of low level seller")
                                    #Schat("changing sellers low level structure because of low level seller")
                                    print("changing sellers low level structure because of low level seller")

                        except IndexError:
                            # Handle the case where the index is out of range
                            print(f"Error: Seller in position {i} doesn't exist.")
                            print(f"Seller number: {i-1}")
                            OutOfRangePosition = i
                            break

                    try:
                        skipOnlineCheck = True
                        for i in range(1, 6):
                            if Seller[i]['name'] == my_name:
                                CurrentlySelling = True
                                #my_pos = i
                                #print("CurrentlySelling = True")
                                if dict_filled and CurrentlySellingOld is False:
                                    print(f"currently selling old is: {CurrentlySellingOld}")
                                    Schat("$tts Back online!")
                                CurrentlySellingOld = True
                                skipOnlineCheck = False
                                break
                        if skipOnlineCheck is True:
                            print("test 21323")
                            CurrentlySelling = False
                            CurrentlySellingOld = False
                            #print("CurrentlySellingOld = False")
                    except IndexError:
                        break

                #    if dict_filled is True:
                #        if CurrentlySellingOld is False:
                #            if Seller[1]['name'] is my_name:
                #                if OldSeller[1]['name'] != my_name:
                #                    if my_pos_old != 1:
                #                        Schat("$tts Back online!")
                #                        CurrentlySellingOld = True
                #    
                #    my_pos_old = my_pos


                    
                elif pre_checkout_sls_offer_div is None:
                    Schat("$tts Price Checker items are none")

            # Testing shift prices
            Testing = False
            if Testing is True:
                TestSeller = {}
                for i in dict_range:
                    try:
                        TestSeller[i] = Seller[i].copy()
                    except KeyError:
                        break
                
                # if price is more then 50
                for i in dict_range:
                    try:
                        TestSeller[i]['price'] = (random.randint(5, 7) / 100) * TestSeller[i]['price']
                        Seller[i]['price'] = (random.randint(5, 7) / 100) * Seller[i]['price']
                        #print(Seller[i])
                    except KeyError:
                        break
                # if price is more then 50
                
                for i in dict_range:
                    try:
                        TestSeller[i]['price'] = (random.randint(85, 100) / 100) * TestSeller[i]['price']
                        Seller[i]['price'] = (random.randint(85, 100) / 100) * Seller[i]['price']
                        print(Seller[i])
                    except KeyError:
                        break




        #    thresholdPercentage = 0.03
        #
        #    medianPrice = (Seller[2]['price'] + Seller[3]['price'] + Seller[4]['price']) / 3
        #    priceDiff = abs(medianPrice - Seller[1]['price'])
        #    print(f"median price of Seller[2-4] is: {medianPrice}")
        #    print(f"price diff is: {priceDiff}")
        #    # Calculate the 3% threshold
        #    #threshold = 0.03 * priceDiff
        #    threshold = thresholdPercentage * priceDiff #testimg
        #    print(f"threshold is: {threshold}")
        #    if priceDiff < thresholdPercentage:
        #        Schat("$tts more then 3 percent price bump")
        #        Schat("more then 3 percent price bump")
        #        print("more then 3 percent price bump")
        #    elif priceDiff > thresholdPercentage:
        #        print("less then 3 percent price NOT bump")

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
                    if Testing is False:
                        try:
                            writer.writerow([Seller[i]['date'], Seller[i]['time'], Seller[i]['price'], Seller[i]['name'], Seller[i]['stock'], Seller[i]['level']])
                        except KeyError:
                            # Write lowest price when loop reaches not existent seller
                            writer.writerow([LowestPrice[i]['date'], LowestPrice[i]['time'], LowestPrice[i]['price'], LowestPrice[i]['name'], LowestPrice[i]['stock'], LowestPrice[i]['level']])
                            break
                    elif Testing is True:
                        try:
                            writer.writerow([TestSeller[i]['date'], TestSeller[i]['time'], TestSeller[i]['price'], TestSeller[i]['name'], TestSeller[i]['stock'], TestSeller[i]['level']])
                        except KeyError:
                            # Write lowest price when loop reaches not existent seller
                            writer.writerow([LowestPrice[i]['date'], LowestPrice[i]['time'], LowestPrice[i]['price'], LowestPrice[i]['name'], LowestPrice[i]['stock'], LowestPrice[i]['level']])
                            break
                    else:
                        print("Write to database failure.")

            NewName = Seller[1]['name']
            NewPrice = Seller[1]['price']
            NewStock = Seller[1]['stock']

            #if dict_filled is True:
            #    print(f"{Seller[1]}")
            #    print(Seller[1]['price'])
            #    print(OldSeller[1])
            #    print(OldSeller[1]['price'])

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

                        #print(f"NewPrice: {NewPrice}")
                        #print(f"OldPrice: {OldPrice}")
                        #print(f"NewStock: {NewStock}")
                        #print(f"OldStock: {OldStock}")


                        ### check for new account
                        if Seller[1]['level'] < 5:
                            skip = True
                            new_account_skip = True


                        print(OldPrice)
                        print(NewPrice)
                        ### price change 
                        if OldPrice > NewPrice and new_account_skip is False:
                            final_price = OldPrice - NewPrice
                            print(f"final price is: {final_price}, old price is: {OldPrice}, price: {NewPrice}")
                            if final_price < 1:
                                final_price_int = int(final_price * 100)
                                if final_price < 0.01:
                                    message = (f"$tts {Seller[1]['name']} stole position")
                                    #Schat(message)
                                    #print(f"### price change  message is: {message}")
                                    skip = True
                                elif final_price < 0.99 and final_price > 0.01:
                                    if final_price_int == 1:
                                        message = f"$tts {Seller[1]['name']} lowered price by {final_price_int} cent"
                                    elif final_price <= 0.99:
                                        message = f"$tts {Seller[1]['name']} lowered price by {final_price_int} cents"
                                    #print(message)
                            else:
                                message = f"$tts {Seller[1]['name']} lowered price by {final_price:.2f} Euro"
                            

#                            if Seller[1]['price'] > 3:
#                                Schat(message)
#                                myprice = Seller[1]['price'] - 0.01
#                                #Schat(f"$tts {myprice:.2f}")
#                                Schat("###########################")
#                                Schat(f"{Seller[1]['name']} new price is: {Seller[1]['price']}")
#                                price_matched = False
#
#
#                                # Input decimal valuemyprice
#                                decimal_value = NewPrice
#
#                                # Convert to a string
#                                decimal_str = str(decimal_value)
#
#                                # Split the string at the decimal point
#                                whole_part, decimal_part = decimal_str.split('.')
#
#                                # Convert the decimal part to an integer and subtract 1
#                                new_decimal_part = str(int(decimal_part) - 1)
#
#                                # Combine the whole part and modified decimal part
#                                new_decimal_str = whole_part + '.' + new_decimal_part
#
#                                # Convert back to a float if needed
#                                new_decreased_price = float(new_decimal_str)
#
#                                Schat(f"Price to copy: {new_decreased_price}")
#                                import pyperclip
#                                pyperclip.copy(str(new_decreased_price))
#
#                                
#                                Schat(f"Set price to {myprice} (-0.01)")
#                                print(f"### price change  message is: {message}")

                            from decimal import Decimal

                            def reduce_price(price):
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
                                    reduced_price = str(reduced_price)
                                
                                
                                return reduced_price

                            new_decreased_price = reduce_price(NewPrice)
                            import pyperclip
                            pyperclip.copy(str(new_decreased_price))
                            Schat(f"New price is {new_decreased_price}")


                            medianPrice = (Seller[2]['price'] + Seller[3]['price'] + Seller[4]['price']) / 3
                            priceDiff = abs(medianPrice - Seller[1]['price'])
                            thresholdPercentage = 0.03
                            if testingPhase:
                                thresholdPercentage = 0.3
                            print(f"median price of Seller[2-4] is: {medianPrice}")
                            print(f"price diff is: {priceDiff}")

                            if priceDiff <= thresholdPercentage or Seller[1]['price'] == Seller[3]['price']:
                            #if final_price <= 0.03 or Seller[1]['price'] == Seller[3]['price']:
                                Schat(f"$tts changing price")
                                Schat(f"tts changing price")
                                Schat(f"Time: {Seller[1]['time']}")

                                import pygetwindow as gw
                                from selenium import webdriver
                                from selenium.webdriver.common.by import By
                                from selenium.webdriver.chrome.options import Options
                                from selenium.webdriver.support.ui import WebDriverWait
                                from selenium.webdriver.support import expected_conditions as EC

                                if TestMethodSelenium == 1:

                                    autoChangePrice = save.controlPanel.autoChangePrice

                                    def switch_to_desktop(desktop_name):
                                        desktop = gw.getWindowsWithTitle(desktop_name)
                                        if desktop:
                                            desktop[0].activate()

                                    if autoChangePrice:
                                        myPage = save.controlPanel.gPriceCheckerURL_myPage
                                        # new_decreased_price = "your_new_price"  # Replace with your desired price

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
                                        try:
                                            # Get the current window handle
                                            original_window_handle = driver.current_window_handle

                                            # Open the G2G URL in a new tab (can be the current tab)
                                            driver.execute_script("window.open('" + myPage + "', '_blank');")

                                            # Switch back to the original tab
                                            driver.switch_to.window(original_window_handle)

                                            # Navigate to the web page
                                            # driver.get(myPage)  # Replace with the URL of the webpage you want to edit

                                            # Wait for the price element to be present on the page
                                            element = WebDriverWait(driver, 10).until(
                                                EC.presence_of_element_located((By.CLASS_NAME, 'g2g_products_price'))
                                            )

                                            # Click on the element to make it editable
                                            element.click()

                                            # Locate the input field for the price
                                            input_field = WebDriverWait(driver, 5).until(
                                                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.input-large'))
                                            )

                                            # Clear the existing value and enter the new price
                                            input_field.clear()
                                            input_field.send_keys(str(new_decreased_price))

                                            # Locate and click the "Save" button
                                            save_button = WebDriverWait(driver, 5).until(
                                                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn--green.editable-submit'))
                                            )

                                            save_button.click()

                                            # Optionally, you can perform further actions on the page after saving the price.

                                        finally:
                                            # Make sure to close the browser, even if there is an exception
                                            driver.quit()
                                
                                if TestMethodSelenium == 2:
                                    autoChangePrice = save.controlPanel.autoChangePrice

                                    if autoChangePrice:
#                                        myPage = save.controlPanel.gPriceCheckerURL_myPage
#
#                                        # Set up Chrome options for connecting to an existing instance
#                                        chrome_options = Options()
#                                        chrome_options.debugger_address = "127.0.0.1:9223"  # Use the desired address and port
#                                        chrome_options.add_argument("--start-maximized")
#
#                                        # Initialize the ChromeDriver with the specified options
#                                        driver = webdriver.Chrome(options=chrome_options)
#
#                                       import subprocess
#
#                                       # Set the path to the Chrome binary and the desired debugging port
#                                       chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
#                                       debugging_port = 9223
#
#                                       # Set the URL of the page you want to interact with
#                                       myPage = save.controlPanel.gPriceCheckerURL_myPage
#
#                                       # Build the command to run Chrome with the desired options
#                                       command = f'"{chrome_path}" --remote-debugging-port={debugging_port} "{myPage}"'
#
#                                       # Use subprocess to run the command in cmd
#                                       subprocess.Popen(command, shell=True)




                                        # Set the desired debugging port
                                        debugging_port = 9223

                                        # Set up Chrome options to run in debugging mode with a specific port
                                        chrome_options = webdriver.ChromeOptions()
                                        chrome_options.add_argument(f'--remote-debugging-port={debugging_port}')

                                        # Initialize the ChromeDriver with the specified options
                                        driver = webdriver.Chrome(options=chrome_options)

                                        # Define the URL of the page you want to interact with
                                        myPage = save.controlPanel.gPriceCheckerURL_myPage

                                        try:
                                            # Navigate to the web page
                                            driver.get(myPage)

                                            # Wait for the price element to be present on the page
                                            element = WebDriverWait(driver, 10).until(
                                                EC.presence_of_element_located((By.CLASS_NAME, 'g2g_products_price'))
                                            )

                                            # Click on the element to make it editable
                                            element.click()

                                            # Locate the input field for the price
                                            input_field = WebDriverWait(driver, 10).until(
                                                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.input-large'))
                                            )

                                            # Clear the existing value and enter the new price
                                            input_field.clear()
                                            input_field.send_keys(new_decreased_price)

                                            # Locate and click the "Save" button
                                            save_button = WebDriverWait(driver, 5).until(
                                                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn.btn--green.editable-submit'))
                                            )

                                            save_button.click()

                                            # Optionally, you can perform further actions on the page after saving the price.

                                        finally:
                                            # Make sure to close the browser, even if there is an exception
                                            driver.quit()

                            elif priceDiff > thresholdPercentage:
                            #elif final_price > 0.03:
                                Schat(f"$tts change price manually")
                                Schat(f"tts change price manually")
                                Schat(f"Time: {Seller[1]['time']}")
                                price_matched = False

                        elif Seller[1]['name'] == my_name or Seller[2]['name'] == my_name and price_matched is False and Seller[1]['price'] == Seller[2]['price']:
                            if Seller[1]['name'] != OldSeller[1]['name'] or Seller[2]['name'] != OldSeller[2]['name']:
                                if Seller[1]['price'] == Seller[2]['price']:
                                    Schat(f"Matched!")
                                    Schat(f"$tts Matched!")
                                    print(f"price matched!")
                                    price_matched = True

                                    # Input decimal valuemyprice
                                    decimal_value = NewPrice

                                    # Convert to a string
                                    decimal_str = str(decimal_value)

                                    # Split the string at the decimal point
                                    whole_part, decimal_part = decimal_str.split('.')

                                    # Convert the decimal part to an integer and subtract 1
                                    new_decimal_part = str(int(decimal_part) - 1)

                                    # Combine the whole part and modified decimal part
                                    new_decimal_str = whole_part + '.' + new_decimal_part

                                    # Convert back to a float if needed
                                    new_decreased_price = float(new_decimal_str)

                                    Schat(f"Price to copy: {new_decreased_price}")
                                    import pyperclip
                                    pyperclip.copy(str(new_decreased_price))









                        elif OldPrice < NewPrice and new_account_skip is False:
                            final_price = NewPrice - OldPrice
                            final_price_int = int(final_price * 100)
                            if final_price < 0.01:
                                message = f"$tts price slightly got higher"
                            elif final_price < 1 and final_price > 0.01:
                                message = f"$tts price got higher by {final_price_int} cents"
                            elif final_price_int == 1:
                                message = f"$tts price got higher by {final_price_int} cent"
                            else:
                                message = f"$tts price got higher by {final_price:.2f} Euro"
                            Schat(message)
                            print(f"### price change  message is: {message}")

                        ### part of stock sold
                        elif OldPrice == NewPrice:
                            if skip is False:
                                if NewName == OldName and NewPrice == OldPrice and NewStock < OldStock:
                                    #print("### part of stock sold Part 1")
                                    #if NewPrice == OldPrice:
                                    #print("### part of stock sold Part 2")
                                    #if NewStock < OldStock:
                                    #print("### part of stock sold Part 1-3")
                                    message = f"$tts {NewName} sold {OldStock - NewStock} divines"
                                    Schat(message)
                                    print(message)
                                    skip = True
                    
                        else:
                            if new_account_skip is False:
                                message = f"$tts {Seller[1]['name']} just matched price"
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
                                message = f"$tts small amount"
                                #Schat(message)
                                print(f"### stock block message is: {message}")
                            elif int(Seller[1]['stock']) > 80:
                                message = f"$tts large quantity"
                                #Schat(message)
                                print(f"### stock block message is: {message}")
                            elif int(Seller[1]['stock']) >= 30:
                                message = f"$tts big stock"
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
                                        message = f"$tts Price difference is {final_price_int} cents"
                                    elif final_price <= 0.01:
                                        message = f"$tts slight price difference"
                                    elif final_price == 0.01:
                                        final_price_int = int(final_price * 100)
                                        message = f"$tts Price difference is {final_price_int} cent"
                                    else:
                                        message = f"$tts Price difference is {final_price:.2f} Euro"
                                    #Schat(message)
                                    print(f"### my name check block message is: {message}")
                                    skip_myname = True

                        if skip_myname is False:
                            if my_name != Seller[1]['name'] and my_name != Seller[2]['name'] and my_name != Seller[3]['name'] and my_name != Seller[4]['name']:
                                message = '$tts You are not in the list!'
                                #Schat(message)
                                print(message)

                    else:
                        print("Nothing has changed")
                        
                elif Seller[1]['name'] == my_name:
                    print(f"{Seller[1]['name']} has the lowest price")

                    #if dict_filled is True
                    if dict_filled is True and Seller[2]['price'] > OldSeller[2]['price'] and my_name == Seller[1]['name'] and Seller[1]['price'] == OldSeller[1]['price']:
                        result =  OldSeller[2]['price'] - Seller[1]['price']
                        if result > 0.02:
                            positionTwoPriceDifference = OldSeller[2]['price'] - Seller[1]['price']
                            Schat(f"$tts position 2 price got higher. Difference {positionTwoPriceDifference:.2f}")

                            NewPrice = Seller[2]['price']
                            decimal_value = NewPrice
                            decimal_str = str(decimal_value)
                            whole_part, decimal_part = decimal_str.split('.')
                            new_decimal_part = str(int(decimal_part) - 1)
                            new_decimal_str = whole_part + '.' + new_decimal_part
                            new_decreased_price = float(new_decimal_str)

                            Schat(f"New pos2 lowered price to copy: {new_decreased_price}")
                            Schat(f"$tts New pos2 lowered price to copy: {new_decreased_price}")
                            import pyperclip
                            pyperclip.copy(str(new_decreased_price))

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
                                        message = f"$tts {target_name} raised price"
                                        print(message)
                                        Schat(message)
                                        break
                                    elif target_price_new < target_price_old:
                                        message = f"{target_name} lowered price"
                                        print(message)
                                        Schat(message)
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

            IterationSleepTime = save.controlPanel.IterationSleepTime
            time.sleep(IterationSleepTime)
    except Exception as e:
        import traceback
        traceback.print_exc()  # Print the traceback to see the error details
        Schat("$tts Error in Price checker!")
        input("PriceChecker got An error. Press Enter to exit...")

#import threading
#PriceChecker = threading.Thread(target=PriceChecker)
#PriceChecker.start()
#PriceChecker()




#1  can't win+d, if you do. When price changes, chrome will get maximized, because it will get minimized on win+d
#2  when price changes u will be left on the tab it changed the price (very left one atm.)
#3  

#1 try using desktop 2


#v2 done. Have to launch two browser windows in desktop 1 and 2. Both must have link open one the very left. Fixes all problems.