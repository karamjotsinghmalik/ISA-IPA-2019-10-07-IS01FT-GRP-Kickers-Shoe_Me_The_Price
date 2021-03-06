'''
1. define valid bots list
2. Execute bots based on that
'''

from robots import footlocker, nike, jdsports, farfetch
import pandas as pd
from send_mail import mail_body_template as mbt
from send_mail import push_mail as pm
from send_mail import price_prediction as pp
from persistence import db_updates as db

'''
Input params -
Output -
'''


def execute_bots_for_mail(mail_list, conn):

    for item in mail_list:
        shoes = item['shoe_names']
        # print(shoes)
        email = item['subscriber_id']
        gender = item['gender']
        if(gender.lower()=='f'):
            gender=' women'
        else:
            gender=' men'

        price_df = pd.DataFrame()
        for shoe in shoes.split(','):

            details = footlocker.get_shoe(shoe, gender, email)
            price_df = price_df.append(details)

            # details = jdsports.get_shoe(shoe, gender, email)
            # price_df = price_df.append(details)

            # details = robots.farfetch.get_shoe(email, shoe, gender = gender)
            # price_df = price_df.append(details)

            ''' if "nike" in shoe.lower():

                details = nike.get_shoe(shoe, gender, email)
                # print('[bot-controller]',details)
                price_df = price_df.append(details)'''

        # get prediction for each shoe
        # print("Price df created")
        # print(price_df.columns)
        price_df = price_df[price_df.name != "NA"]
        # print("NA removed")
        if len(price_df) != 0:
            # print("LEN not 0")
            price_df_final = pp.price_trend(price_df, conn)
            # print("price trend extracted")
        # print('[bot-controller]','after price_df assignment')
            mail_body = mbt.mail_template(price_df_final)
        # print('[bot-controller] mailbody ready')
        else:
            mail_body = '''<html>
                <body>Sorry, We couldn't find any shoes matching your request.<br>
            Please send us a mail at shoemetheprice@gmail.com with the shoe name and gender in the subject.<br>
            Example subject - [M] Nike Air Max 1<br><br>

            Thank You<br>
            ShoeMeThePrice<body><html>'''
            print("Sorry mail body ready")

    # NEED TO CALL SEND MAIL WITH mail_body AS ARGUMENT
        service = pm.connect_gmail_send()
        message = pm.create_message(email, shoes, mail_body)
        pm.send_message(service, message)
        db.push_price_data(price_df,conn)
        # print("Data pushed")

    return


def execute_bots_for_daily(inp_details, conn):
    

    for i in range(0, len(inp_details)):
        price_df = pd.DataFrame()
        email = inp_details['subscriber_id'][i]
        shoes = inp_details['shoe_names'][i]
        gender = inp_details['gender'][i]

        if gender.lower() == "f":
            gender = ' women'
        else:
            gender = ' men'

        for shoe in shoes.split(','):

            if "nike" in shoe.lower():
                details = nike.get_shoe(shoe, gender, email)
                price_df = price_df.append(details)

            details = footlocker.get_shoe(shoe, gender, email)
            price_df = price_df.append(details)

            details = jdsports.get_shoe(shoe, gender, email)
            price_df = price_df.append(details)

            details = farfetch.get_shoe(shoe, gender, email)
            price_df = price_df.append(details)

            

        # get prediction for each shoe

        price_df = price_df[price_df['name'] != "NA"]

        if len(price_df) != 0:

            price_df_final = pp.price_trend(price_df, conn)
        # print('[bot-controller]','after price_df assignment')
            mail_body = mbt.mail_template(price_df_final)
        # print('[bot-controller] mailbody ready')
        else:
            mail_body = '''<html>
                <body>Sorry, We couldn't find any shoes matching your request.<br>
            Please send us a mail at shoemetheprice@gmail.com with the shoe name and gender in the subject.<br>
            Example subject - [M] Nike Air Max 1<br><br>

            Thank You<br>
            ShoeMeThePrice</body></html>'''

    # NEED TO CALL SEND MAIL WITH mail_body AS ARGUMENT
        service = pm.connect_gmail_send()
        message = pm.create_message(email, shoes, mail_body)
        pm.send_message(service, message)
        db.push_price_data(price_df,conn)
        # print("Data pushed")
       
        
        db.update_status(inp_details.iloc[i], conn)

    return
