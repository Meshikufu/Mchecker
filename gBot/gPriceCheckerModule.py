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
    time.sleep(5*0)
    try:

        def process_sellerInfo(sellerInfo):
            date_str, current_time_str = date_Database()

            stock_str = sellerInfo.find('div', class_='offers-top-tittles', string='Stock').find_next('span').text.strip()
            level_str = sellerInfo.find('div', class_='seller_level-peronal').text
            seller_list = {
                'name': sellerInfo.find('div', class_='seller__name-detail').text,
                'level': int(level_str.replace('Level ', '')),
                #'delivery_method': sellerInfo.find('div', class_='offers-top-tittles', string='Delivery method').find_next('div', class_='tippy').text.strip(),
                #'delivery_speed': sellerInfo.find('div', class_='offers-top-tittles', string=' Delivery speed').find_next('span').text.strip(),
                'stock': int(stock_str.replace(',', '').replace('Mil', '')),
                #'stock': int(stock_str.replace('Mil', '')),
                #'min_purchase': sellerInfo.find('div', class_='offers-top-tittles', string='Min. purchase').find_next('span').text.strip(),
                'price': float(sellerInfo.find('span', class_='offer-price-amount').text),
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
        my_name = save.controlPanel.my_name
        target_name = save.controlPanel.target_name
        
        

        ### TEST SWITCH
        test_phase = save.controlPanel.test_phase
        test_number = 1

        while True:

            if test_phase == False:
                IterationSleepTime = random.randint(600, 900) 

                url = save.controlPanel.gPriceCheckerURL
                response = requests.get(url)
                html_content = response.text

                soup = BeautifulSoup(html_content, 'html.parser')

                pre_checkout_sls_offer_div = soup.find('div', {'id': 'pre_checkout_sls_offer', 'class': 'hide'})
                other_seller_offer_mainboxes = pre_checkout_sls_offer_div.find_all('div', {'class': 'other-seller-offeer_mainbox'})
                other_seller_offer_mainboxes = other_seller_offer_mainboxes[0]


                Seller = {}
                for i in dict_range:
                    try:
                        Seller[i] = process_sellerInfo(other_seller_offer_mainboxes.find_all('div', {'class': 'other_offer-desk-main-box other_offer-div-box'})[i-1])
                        print(f"Seller[{i}]: {Seller[i]}")
                    except IndexError:
                        # Handle the case where the index is out of range
                        print(f"Error: Seller in position {i} doesn't exist.")
                        print(f"Seller number: {i-1}")
                        OutOfRangePosition = i
                        break


#            elif test_phase == True:
#                IterationSleepTime = 20
#
#                import json
#
#                print(test_number)
#
#                if test_number == 1:
#                    with open(rf'C:\Users\Kufu\PythonProjects\Mchecker\gBot\t1.json', 'r') as json_file:
#                        dataTest = json.load(json_file)
#                if test_number == 2:
#                    with open(rf'C:\Users\Kufu\PythonProjects\Mchecker\gBot\t2.json', 'r') as json_file:
#                        dataTest = json.load(json_file)
#                if test_number == 3:
#                    with open(rf'C:\Users\Kufu\PythonProjects\Mchecker\gBot\t3.json', 'r') as json_file:
#                        dataTest = json.load(json_file)
#                if test_number == 4:
#                    with open(rf'C:\Users\Kufu\PythonProjects\Mchecker\gBot\t4.json', 'r') as json_file:
#                        dataTest = json.load(json_file)
#                if test_number == 5:
#                    with open(rf'C:\Users\Kufu\PythonProjects\Mchecker\gBot\t5.json', 'r') as json_file:
#                        dataTest = json.load(json_file)
#                    test_number = 0
#                    
#
#                test_number += 1
#
#                # Extract data into separate dictionaries
#                Seller[1] = dataTest['seller1']
#                Seller[2] = dataTest['seller2']
#                Seller[3] = dataTest['seller3']
#                Seller[4] = dataTest['seller4']
#
#                # Print the extracted dictionaries
#                print("Seller 1:", Seller[1])
#                print("Seller 2:", Seller[2])
#                print("Seller 3:", Seller[3])
#                print("Seller 4:", Seller[4])


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
                        writer.writerow([Seller[i]['date'], Seller[i]['time'], Seller[i]['price'], Seller[i]['name'], Seller[i]['stock']])
                    except KeyError:
                        # Write lowest price when loop reaches not existent seller
                        writer.writerow([LowestPrice[i]['date'], LowestPrice[i]['time'], LowestPrice[i]['price'], LowestPrice[i]['name'], LowestPrice[i]['stock']])
                        break

            NewName = Seller[1]['name']
            NewPrice = Seller[1]['price']
            NewStock = Seller[1]['stock']


            if Seller[1]['name'] != my_name and dict_filled == True:
                # checking if seller with lowest price is still with lowest price
                if Seller[1]['name'] != OldSeller[1]['name'] or Seller[1]['price'] != OldSeller[1]['price'] or Seller[1]['stock'] != OldSeller[1]['stock']:
                    skip = False
                    skip_myname = False
                    new_account_skip = False
                    print(skip)
                    print(f"OldSeller[1]['price']: {OldSeller[1]['price']}")
                    print(f"Seller[1]['price']: {Seller[1]['price']}")
                    print(f"OldSeller[1]['stock']: {OldSeller[1]['stock']}")
                    print(f"Seller[1]['stock']: {Seller[1]['stock']}")

                    print(f"NewPrice: {NewPrice}")
                    print(f"OldPrice: {OldPrice}")
                    print(f"NewStock: {NewStock}")
                    print(f"OldStock: {OldStock}")


                    ### check for new account
                    if Seller[1]['level'] < 5:
                        skip = True
                        new_account_skip = True


                    ### price change 
                    if OldPrice > NewPrice and new_account_skip == False:
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
                        Schat(message)
                        print(f"### price change  message is: {message}")


                    elif OldPrice < NewPrice and new_account_skip == False:
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
                        if skip == False:
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
                        if new_account_skip == False:
                            message = f"$tts {Seller[1]['name']} just matched price"
                            print(message)
                            #Schat(message)
                            skip = True


                    ### if first position seller sold all his stock
                    if skip == False and new_account_skip == False:
                        if Seller[1]['name'] == OldSeller[2]['name'] and Seller[1]['stock'] == OldSeller[2]['stock'] and Seller[1]['price'] == OldSeller[2]['price']:
                            message = f"{OldSeller[1]['name']} sold all {OldSeller[1]['stock']} divines"
                            message = f"pos 1 sold everything or went offline"
                            #Schat(message)
                            print(f"### if first position seller sold all his stock message is: {message}")
                            skip = True


                    ### stock block
                    if skip == False and new_account_skip == False:
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
                    if skip == False and new_account_skip == False:
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

                    if skip_myname == False:
                        if my_name != Seller[1]['name'] and my_name != Seller[2]['name'] and my_name != Seller[3]['name'] and my_name != Seller[4]['name']:
                            message = '$tts You are not in the list!'
                            #Schat(message)
                            print(message)

                else:
                    print("Nothing has changed")
                    
            elif Seller[1]['name'] == my_name:
                print(f"{Seller[1]['name']} has the lowest price")

            target_name_trigger  = 0
            target_name_trigger_cell1 = False
            target_name_trigger_cell2 = False

            if dict_filled == True:
                for i in dict_range:
                    if target_name_trigger_cell1 == False:
                        try:
                            if Seller[i]['name'] == target_name:
                                target_price_new = Seller[i]['price']
                                target_name_trigger += 1
                                target_name_trigger_cell1 = True
                                print(f"{target_name} test cell 1: {target_price_new} and {Seller[i]['price']}")
                        except KeyError:
                            print(f"Error: cell 1 Seller in position {i} doesn't exist.")
                            break
                    if target_name_trigger_cell2 == False:
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

            time.sleep(IterationSleepTime)
    except Exception as e:
        import traceback
        traceback.print_exc()  # Print the traceback to see the error details
        input("PriceChecker got An error. Press Enter to exit...")

#import threading
#PriceChecker = threading.Thread(target=PriceChecker)
#PriceChecker.start()
#PriceChecker()