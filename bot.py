#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import pickle
import os

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,ConversationHandler)
from firebase import firebase
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import tree
# X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
# # y = 1 * x_0 + 2 * x_1 + 3
# y = np.dot(X, np.array([1, 2])) + 3
import numpy as np
import urllib
import pandas as pd  # To read data
# URL for the Pima Indians Diabetes dataset (UCI Machine Learning Repository)
import csv
# Enable logging


arr_answers = []
answers=""
firebase = firebase.FirebaseApplication('https://telegrambot-74c3b-default-rtdb.firebaseio.com/', None)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

ANSWER1,ANSWER2,ANSWER3,ANSWER4= range(4)


def mlCode(distance,bathroom,sleepingroom,lat,long):
    data = pd.read_csv('OpenSouqRealEstate.csv')  # load data set
    X = data.iloc[:, 1:6].values # values converts it into a numpy array
    Y = data.iloc[:, 0].values # -1 means that calculate the dimension of rows, but have 1 column
    linear_regressor = tree.DecisionTreeClassifier()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    #print(linear_regressor.score(X, Y))
    #print(X)
    Y_pred = linear_regressor.predict([[distance,bathroom,sleepingroom,lat,long]])  # make predictions
    return Y_pred


def start(update, context):
    user = update.message.from_user
    print(user.id)
    os.remove(str(user.id)+'.dat') 
    update.message.reply_text(
        'مرحبا انا عقار بوت (كم مساحة البيت المرغوب به)؟')
    return ANSWER1


def answer1(update, context):
    user = update.message.from_user
    logger.info("Answer1 of %s: %s", user.first_name, update.message.text)
    arr_answers.append(update.message.text)
    with open(str(user.id)+'.dat','wb') as wfp:
        pickle.dump(arr_answers, wfp)
    update.message.reply_text('كم حمام ؟')

    return ANSWER2

def answer2(update, context):
    user = update.message.from_user
    logger.info("Answer1 of %s: %s", user.first_name, update.message.text)
    arr_answers.append(update.message.text)
    with open(str(user.id)+'.dat','wb') as wfp:
        pickle.dump(arr_answers, wfp)
    update.message.reply_text('كم عدد غرف النوم؟')

    return ANSWER3
    
def answer3(update, context):
    user = update.message.from_user
    logger.info("Answer1 of %s: %s", user.first_name, update.message.text)
    arr_answers.append(update.message.text)
    with open(str(user.id)+'.dat','wb') as wfp:
        pickle.dump(arr_answers, wfp)
    update.message.reply_text('اين يقع العقار؟ اختار لوكيشن او مكان ؟')

    return ANSWER4

  
def answer4(update, context):
    user = update.message.from_user
    user_location = update.message.location
    print(user_location)
    with open(str(user.id)+'.dat','rb') as rfp:
        arr_answers = pickle.load(rfp)
        logger.info(arr_answers)
    price=mlCode(arr_answers[-3],arr_answers[-2],arr_answers[-1],user_location.longitude,user_location.latitude)
    # firebase.post('/telegram_bot_users/'+str(user.id),{'answers':arr_answers})
    # result = firebase.get('/telegram_bot_users/'+str(user.id), None)
    update.message.reply_text("السعر المتوقع"+str(price[0])+  "دولار"  "\n شكرا لك على اختيانا يمكنك زيارة مقر الشركة حسب العنوان من الساعة 10ص الى الساعة 9 مسا""")

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater('1693457418:AAEir2pTmISLv2iCajlD9myKEuP10j4X6a0', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            ANSWER1: [MessageHandler(Filters.text, answer1)],

            ANSWER2: [MessageHandler(Filters.text, answer2)],
            ANSWER3: [MessageHandler(Filters.text, answer3)],
            ANSWER4:  [
                MessageHandler(Filters.location, answer4),
              
            ]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()