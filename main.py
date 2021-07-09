import asyncio
import concurrent.futures
import datetime
import logging
import sys
import time
import traceback

import discord
from discord import Intents
from discord.ext import tasks
from github import Github

import crypttrack

# TODO ADD START UP FUNCTION TO DELETE ALL PREVIOUS MESSAGES IN TICKER CHANNEL!
g = Github('') #GITHUB INFO HERE
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = Intents.all()
client = discord.Client(intents=intents)

global all_coin
all_coin = {}
doge_token = '0xbA2aE424d960c26247Dd6c32edC70B295c744C43'
global flag_list_percent
flag_list_percent = []
global delta_list
delta_list = {}
global flag_list_percent_text
flag_list_percent_text = 'flags/flag_list_percent.txt'
global delta_list_txt
delta_list_txt = 'delta/delta_list.txt'


def import_crypto_list(text, my_list):
    text = open(text, encoding='utf-8', mode='r')
    for line in text:
        line = line.strip()
        line = line.split(' ', 1)
        if len(line) < 2:
            continue
        if crypttrack.isfloat(line[0]):
            temp_dic = {float(line[0]): line[1]}
            my_list.append(temp_dic)
        else:
            temp_dic = {line[0]: line[1]}
            my_list.append(temp_dic)


def delta_update_text(text, my_dict):
    str_temp = ''
    for k, v in my_dict.items():
        str_temp = str_temp + f'{k} {v}\n'
    repo = g.get_repo('ghostofcoolidge/cryptobot')
    contents = repo.get_contents(text)
    repo.update_file(contents.path, 'update', str_temp, contents.sha)


def delta_update_list(text):
    temp_dict = {}
    repo = g.get_repo('ghostofcoolidge/cryptobot')
    contents = repo.get_contents(text)
    # print(f' contents: {contents.decoded_content}\n\n')
    te = str(contents.decoded_content).replace('b"', '').replace("'b'", '').rstrip('"').rsplit(r'\n', 1)[0].split(r'\n')
    # print(f'delta github contents: {te}')
    # print(len(te))
    # print(te[0])
    # print(te[1])
    for item in te:
        # print(item)
        if item == '' or item == "b'" or item == "'" or item.startswith('b'):
            continue
        else:
            ti2 = item.replace(',', '').replace('\n', '').replace("'", '').replace('"', '')
            user, ti2 = ti2.split(' [[')
            li = []
            # print(ti2)
            ti2 = ti2.replace(']]', '').split('] [')
            # print(ti2)
            for tempitem in ti2:
                li2 = []
                # print(item)
                tempitem = tempitem.split()
                # print(item)
                for it in tempitem:
                    if crypttrack.isfloat(it):
                        li2.append(float(it))
                    else:
                        li2.append(it)
                li.append(li2)
            temp_dict.update({int(user): li})
    return temp_dict


delta_list = delta_update_list(delta_list_txt)
print(f'DELTA LIST: {delta_list}')
print(len(delta_list))


def flag_list(fl, flagtext):
    try:
        repo = g.get_repo('ghostofcoolidge/cryptobot')
        contents = repo.get_contents(flagtext)
        item = str(contents.decoded_content).lstrip("b'")
        item = item.strip()
        item = ''.join(item)
        if item == '':
            return []
        i = item.split(',')
        for it in i:
            temp_dict = {}
            if 'user' not in it:
                continue
            j = it.split(r'\n')
            for k in j:
                if k == '':
                    continue
                k = k.split(' ')
                if k[1].isdigit():
                    k[1] = int(k[1])
                elif crypttrack.isfloat(k[1]):
                    k[1] = float(k[1])
                temp_dict.update({k[0]: k[1]})
            fl.append(temp_dict)
    except Exception:
        x, y, z = sys.exc_info()
        print(y)
        z = (traceback.format_tb(z))
        print(z)


flag_list(flag_list_percent, flag_list_percent_text)
print(flag_list_percent)


def coin_list():
    all_coins = []
    repo = g.get_repo('ghostofcoolidge/cryptobot')
    contents = repo.get_contents('crypt')
    for item in contents:
        temp_dict = {}
        temp_dict.update({'path': item.path})
        item = str(item.decoded_content).split("b'", 1)[1]
        item = item.rstrip(r"'")
        item = item.split('\\n')
        for i in item:
            if len(i) < 1:
                continue
            i = i.split(' ', 1)
            temp_dict.update({i[0]: i[1]})
        all_coins.append(temp_dict)
    print(all_coins)
    return all_coins


all_coin = coin_list()


def update_flag_text(flli, flagtext):
    print('updating flag text...')
    strlist = ''
    for item in flli:
        for k, v in item.items():
            strlist = strlist + str(k) + f' {str(v)}\n'
        strlist = strlist + ','
    repo = g.get_repo(f'ghostofcoolidge/cryptobot')
    contents = repo.get_contents(flagtext)
    repo.update_file(contents.path, 'update', strlist, contents.sha)
    print('done')


# TODO PUT ALL COINS INTO ONE LIST AS DICTIONARIES AND ONE FILE ON GITHUB
def update_coin_text(clist):
    print('updating coin text...')
    strlist = ''
    for k, v in clist.items():
        strlist = strlist + str(k) + f' {str(v)}\n'
    repo = g.get_repo(f'ghostofcoolidge/cryptobot')
    contents = repo.get_contents(clist["path"])
    repo.update_file(contents.path, 'update', strlist, contents.sha)
    print('done')


@client.event
async def on_message(message):
    global all_coin, delta_list, prev_mess
    sub = []

    def substring(var):
        var = var.lower()
        if var.startswith("$crypto "):
            sub.append(31)
        elif var == '$hold':
            sub.append(32)
        elif var.startswith("$add"):
            sub.append(33)
        elif var.startswith("$delta"):
            sub.append(34)
        elif var.startswith("$flag"):
            sub.append(35)
        elif var.startswith("$remove"):
            sub.append(36)
        else:
            return None
        return sub

    # if message.author == client.user and message.channel.id == 833260021642690590:
    #     prev_mess.append(message)
    #     print('previous message grabbed')
    if message.author == client.user or message.author.id == 312807432839626753 or message.author.id == 235088799074484224 or message.author.id == 252128902418268161 or message.author.id == 172002275412279296:
        return
    if message.author.name is None:
        return
    if message.author.id is None:
        return
    try:
        if isinstance(message.channel, discord.channel.DMChannel):
            mess = message.content.split()
            mess = ' '.join(mess)
            if mess.startswith('$delta add'):
                await message.author.send('adding crypto to delta list...')
                parse = mess.split()
                if len(parse) != 5:
                    await message.channel.send('incorrect number of argument given')
                    return
                user = message.author.id
                token = crypttrack.parse_BNB_token(parse[2])
                if token is False:
                    await message.channel.send('could not parse token name from bsc')
                    return
                token_id = parse[2]
                amount = float(parse[3].replace(',', ''))
                BNB = parse[4].replace(',', '')
                if user not in delta_list:
                    flag = 1
                    temp_list = [token, token_id, amount, BNB, flag]
                    delta_list.update({user: [temp_list]})
                    print(delta_list)
                else:
                    flag = len(delta_list[user]) + 1
                    temp_list = [token, token_id, amount, BNB, flag]
                    delta_list[user].append(temp_list)
                    print(delta_list)
                delta_update_text(delta_list_txt, delta_list)
                await message.author.send(f'Added {token} to delta list! Flag number is: {flag}')
                return
            elif mess.startswith('$delta remove'):
                parse = mess.split()
                if len(parse) == 3 and parse[-1].isdigit():
                    flag = float(parse[-1])
                    user = message.author.id
                    print(len(delta_list[user]))
                    delta_found = False
                    for k, v in delta_list.items():
                        if user == int(k):
                            for it in v:
                                if flag in it:
                                    delta_found = True
                                    break
                        if delta_found:
                            if len(delta_list[user]) > 1:
                                v.remove(it)
                                await message.channel.send('delta has been removed!')
                                delta_update_text(delta_list_txt, delta_list)
                                return
                            else:
                                delta_list.pop(user)
                                await message.channel.send('delta has been removed!')
                                delta_update_text(delta_list_txt, delta_list)
                                return
            elif mess.startswith('$delta'):
                user = message.author.id
                if user not in delta_list.keys():
                    await message.channel.send('you currently do not have token deltas being tracked')
                temp_set = set()
                stri = ''
                print(f'delta list: {delta_list[user]}')
                if len(delta_list[user]) < 2:
                    current_val_BNB = (crypttrack.get_token_bnb_value(delta_list[user][0][1]))
                    print(f'current bnb val: {decimal_str(current_val_BNB)}')
                    old_BNB_val = float(delta_list[user][0][3]) / float(delta_list[user][0][2])
                    print(f'old bnb val: {decimal_str(old_BNB_val)}')
                    percentage = round(float(((current_val_BNB - old_BNB_val) / old_BNB_val) * 100), 2)
                    if percentage > 0:
                        stri = stri + f'{delta_list[user][0][0]} has increased in value by {percentage}% since your initial purchase!!\n'
                    if percentage < 0:
                        stri = stri + f'{delta_list[user][0][0]} has decreased in value by {percentage}% since your initial purchase!!\n'
                    await message.author.send(stri)
                    return
                else:
                    for item in delta_list[user]:
                        temp_string = ''
                        current_val_BNB = crypttrack.get_token_bnb_value(item[1])
                        print(f'current bnb val: {decimal_str(current_val_BNB)}')
                        old_val_bnb = float(item[3]) / float(item[2])
                        print(f'old bnb val: {decimal_str(old_val_bnb)}')
                        percentage = round(float(((current_val_BNB - old_val_bnb) / old_val_bnb) * 100), 2)
                        if percentage > 0:
                            temp_string = temp_string + f'{item[0]} has increased in value by {percentage}% since your initial purchase!!! flag: {item[-1]}'
                        if percentage < 0:
                            temp_string = temp_string + f'{item[0]} has decreased in value by {percentage}% since your initial purchase!!! flag: {item[-1]}'
                        temp_set.add(temp_string)
                    print(temp_set)

                    def sort(e):
                        e = e.split('% since your initial purchase!!!', 1)[0].split('value by ')[1]
                        return float(e)

                    sorted_list = sorted(temp_set, key=sort, reverse=True)
                    for item in sorted_list:
                        stri = f'{stri}{item}\n'
                    await message.channel.send(stri)
                    return
        else:
            message_current_coin = message.content
            print(message_current_coin)
            substring(message_current_coin)
            if 36 in sub:
                if message.author.id == 95673101429243904 or message.author.id == 797387782766592020:
                    remove = message_current_coin.strip().split(' ')
                    print(remove)
                    if len(remove) == 2:
                        name = remove[1]
                        token_found = await crypttrack.remove_token_get(name, g, client)
                        if token_found:
                            all_coin = coin_list()
                            await message.channel.send('token removed')
                            return
                        await message.channel.send('token not found in archive!')
                        return
                    await message.channel.send('incorrect amount of arguments given')
            if 34 in sub:
                parse = message_current_coin.strip().split(' ')
                if len(parse) == 4:
                    token_name = crypttrack.parse_BNB_token(parse[1])
                    if token_name:
                        current_val_BNB = crypttrack.get_token_bnb_value(parse[1])
                        print(f'current bnb val: {decimal_str(current_val_BNB)}')
                        old_BNB_val = float(parse[3]) / float(parse[2])
                        print(f'old bnb val: {decimal_str(old_BNB_val)}')
                        percentage = round(float(((current_val_BNB - old_BNB_val) / old_BNB_val) * 100), 2)
                        if percentage >= 0:
                            await message.channel.send(
                                f'{token_name} has increased by {percentage}% since your initial purchase! (bnb)')
                            return
                        if percentage < 0:
                            await message.channel.send(
                                f'{token_name} has decreased by {percentage}% since your initial purchase! (bnb)')
                            return
                    else:
                        await message.channel.send('could not parse token name from BSCscan')
                else:
                    await message.channel.send('invalid number of arguments')
            if 35 in sub:
                parse = message_current_coin.strip().split(' ')
                if len(parse) == 3:
                    if parse[2].endswith("%"):
                        try:
                            token = parse[1]
                            flag_percent = float(parse[2].rstrip('%'))
                            mess = crypttrack.add_flag_percent(message, all_coin, token, flag_percent,
                                                               flag_list_percent)
                            if mess == 'please use a number other than zero' or mess == 'token not found in list: please choose a token that is being tracked by the bot':
                                await message.channel.send(mess)
                                return
                            await message.channel.send(mess)
                            update_flag_text(flag_list_percent, flag_list_percent_text)
                            return
                        except Exception:
                            try:
                                err_message = client.get_user(797387782766592020)
                                x, y, z = sys.exc_info()
                                z = (traceback.format_tb(z))
                                await err_message.send(z)
                                await err_message.send(y)
                            except Exception:
                                err_message = client.get_user(797387782766592020)
                                x, y, z = sys.exc_info()
                                z = (traceback.format_tb(z))
                                print(y)
                                print(z)
                                await err_message.send('error too long to send through discord; please check Heroku')
                    else:
                        await message.channel.send('must be a percentage increase/decrease')
                else:
                    await message.channel.send('incorrect number of arguments')
            if 31 in sub:
                parse = message_current_coin.split()
                parse = ' '.join(parse)
                parse = parse.replace('$crypto ', '')
                print(f'parse: {parse}')
                if parse.startswith('delta'):
                    parse_split = parse.split(' ')
                    print(len(parse_split))
                    if len(parse_split) != 5:
                        await message.channel.send('Incorrect amount of arguments')
                        return
                    current_val_BNB = crypttrack.get_token_bnb_value(parse_split[2])
                    print(f'current bnb val: {decimal_str(current_val_BNB)}')
                    old_BNB_val = float(parse_split[4]) / float(parse_split[3])
                    print(f'old bnb val: {decimal_str(old_BNB_val)}')
                    percentage = round(float(((current_val_BNB - old_BNB_val) / old_BNB_val) * 100), 2)
                    if percentage > 0:
                        await message.channel.send(
                            f'{parse_split[1]} has increased by {percentage}% since your initial purchase! (bnb)')
                        return
                    if percentage < 0:
                        await message.channel.send(
                            f'{parse_split[1]} has decreased by {percentage}% since your initial purchase! (bnb)')
                        return
                if parse.startswith('add flag'):
                    add_flag = message_current_coin.split()
                    if len(add_flag) != 5:
                        await message.channel.send(
                            'incorrect number of arguments:\nto add a flag, please do the following:')
                        await message.channel.send('type *$crypto add flag TOKENNAME PERCENTAGE*')
                        return
                    print(add_flag)
                    if parse.endswith('%'):
                        try:
                            token = add_flag[3].upper()
                            flag_percent = float(add_flag[4].rstrip('%'))
                            mess = crypttrack.add_flag_percent(message, all_coin, token, flag_percent,
                                                               flag_list_percent)
                            if mess == 'please use a number other than zero':
                                await message.channel.send(mess)
                                return
                            await message.channel.send(mess)
                            update_flag_text(flag_list_percent, flag_list_percent_text)
                            return
                        except Exception:
                            try:
                                err_message = client.get_user(797387782766592020)
                                x, y, z = sys.exc_info()
                                z = (traceback.format_tb(z))
                                await err_message.send(z)
                                await err_message.send(y)
                            except Exception:
                                err_message = client.get_user(797387782766592020)
                                x, y, z = sys.exc_info()
                                z = (traceback.format_tb(z))
                                print(y)
                                print(z)
                                await err_message.send('error too long to send through discord; please check Heroku')
                    else:
                        await message.channel.send('type *$crypto add flag TOKENNAME PERCENTAGE*')
                elif parse.startswith('add'):
                    if message.author.id == 95673101429243904 or message.author.id == 797387782766592020:
                        add = message_current_coin.split(' ')
                        # print(add)
                        if len(add) != 4:
                            await message.channel.send(
                                'incorrect number of arguments:\n to add a coin, please do the following:')
                            await message.channel.send('type "**$crypto add *(name of token) (token id)*')
                            return
                        name = add[2].upper()
                        # print(name)
                        token = add[3]
                        # print(token)
                        token_check = crypttrack.check_BNB_token(token)
                        if token_check:
                            await crypttrack.add_token_git(name, token, g, message)
                            all_coin = coin_list()
                            for item in all_coin:
                                if item["token"] == token:
                                    curr_time = datetime.datetime.now()
                                    first_value = crypttrack.direct_coin_request(token, item["Name"])
                                    item.update({first_value: curr_time})
                                    update_coin_text(item)
                            await message.channel.send(f'{name} has been added to the crypto tracker!')
                            return
                        else:
                            await message.channel.send('bad token; please find a new token and try again')
                            return
                # if parse.startswith('remove flag'):
                #     remove_flag = message_current_coin.split(' ')
                #     if len(remove_flag) != 4:
                #         await message.channel.send(
                #             'incorrect number of arguments:\nto remove a flag, please do the following:')
                #         await message.channel.send('type *$crypto remove flag FLAGNUMBER*')
                #         return
                #     if remove_flag[-1].isnum():
                #         try:
                #             flagnum = int(remove_flag[-1])
                #             await crypttrack.remove_flag(message, flag_list_percent, flagnum)
                #             update_flag_text(flag_list_percent, flag_list_percent_text)
                #         except Exception:
                #             err_message = client.get_user(797387782766592020)
                #             x, y, z = sys.exc_info()
                #             print(y)
                #             print(z)
                #             z = (traceback.format_tb(z))
                #             await err_message.send(z)
                #             await err_message.send(y)
                if parse.startswith('remove'):
                    await message.channel.send('removing token from archive')
                    if message.author.id == 95673101429243904 or message.author.id == 797387782766592020:
                        remove = message_current_coin.split(' ')
                        print(remove)
                        if len(remove) != 3:
                            await message.channel.send('incorrect amount of arguments given')
                            return
                        name = remove[2].upper()
                        token_found = await crypttrack.remove_token_get(name, g, client)
                        if token_found:
                            all_coin = coin_list()
                            await message.channel.send('token removed')
                            return
                        await message.channel.send('token not found in archive!')
                elif parse.endswith('all'):
                    for item in all_coin:
                        value = crypttrack.direct_coin_request(item['token'], item["Name"])
                        value = decimal_str(value, 15)
                        await message.channel.send(f'current {item["Name"]}: ${value}')
                    return
                for item in all_coin:
                    if item["Name"].lower() == parse.split(' ')[0]:
                        if parse.endswith(item["Name"]):
                            value = crypttrack.direct_coin_request(item['token'], item["Name"])
                            value = decimal_str(value, 15)
                            await message.channel.send(f'current {item["Name"]}: ${value}')
                            return
                        if parse.endswith('hourly'):
                            await crypttrack.hourly(item, message)
                            return
                        if parse.endswith('daily'):
                            await crypttrack.daily(item, item['token'], item["Name"], message)
                            return
                        if parse.endswith('daily'):
                            await crypttrack.weekly(item, item['token'], item["Name"], message)
                            return
                        if parse.endswith('monthly'):
                            await crypttrack.monthly(item, item['token'], item["Name"], message)
                        return
            elif 32 in sub:
                hold = client.get_channel(833260021642690590)
                await hold.send('hold')
            if message_current_coin == "$test":
                for item in all_coin:
                    qpc, new, old, perc = crypttrack.percent_check_quarterly(item, 15)
                    if qpc:
                        if perc > 0:
                            channel_message = client.get_channel(830985148207202324)
                            await channel_message.send(
                                f'@everyone\nValue of {item["Name"]} increased over 15% over the past 6 hours:\n**OLD: **{decimal_str(old)}\n**NEW**: {decimal_str(new)}\n*({perc})%*')
                        if perc < 0:
                            channel_message = client.get_channel(830654217081454673)
                            await channel_message.send(
                                f'@everyone\nValue of {item["Name"]} decreased over 15% over the past 6 hours:\n**OLD: **{decimal_str(old)}\n**NEW**:{decimal_str(new)}\n*({perc})%*')
            elif 33 in sub:
                if message.author.id == 95673101429243904 or message.author.id == 797387782766592020:
                    add = message_current_coin.strip().split(' ')
                    if len(add) != 2:
                        await message.channel.send('invalid number of arguments')
                        return
                    token = add[1]
                    token_check = crypttrack.check_BNB_token(token)
                    print(token_check)
                    token_BINANCE_check = crypttrack.check_BINANCE_token(token)
                    print(token_BINANCE_check)
                    token_uni_check = crypttrack.check_uni_token(token)
                    if token_check:
                        token_name = crypttrack.parse_BNB_token(token)
                        if token_name:
                            await crypttrack.add_token_git(token_name, token, g, message)
                            all_coin = coin_list()
                            for item in all_coin:
                                if item["token"] == token:
                                    curr_time = datetime.datetime.now()
                                    first_value = crypttrack.direct_coin_request(token, token_name)
                                    item.update({first_value: curr_time})
                                    update_coin_text(item)
                                    await message.channel.send(f'{token_name} has been added to the crypto tracker!')
                                    return
                            else:
                                await message.channel.send('sorry; could not parse name from bscscan; please manually add token name and token_id')
                                return
                    elif token_BINANCE_check or token_uni_check:
                        await message.channel.send('searching for ERC token')
                        token_name = crypttrack.parse_ERC_token(token)
                        if token_name:
                            await message.channel.send('found ERC token')
                            await crypttrack.add_token_git(token_name, token, g, message)
                            all_coin = coin_list()
                            for item in all_coin:
                                if item["token"] == token:
                                    curr_time = datetime.datetime.now()
                                    first_value = crypttrack.direct_coin_request(token, token_name)
                                    item.update({first_value: curr_time})
                                    update_coin_text(item)
                                    await message.channel.send(f'{token_name} has been added to the crypto tracker!')
                                    return
                            else:
                                await message.channel.send(
                                    'sorry; could not parse name from etherscan; please manually add token name and token_id')
                                return
                    else:
                        await message.channel.send('bad token; Could not find token on Binance exchange or Binance Smart chain.')
                        return
    except:
        try:
            err_message = client.get_user(797387782766592020)
            x, y, z = sys.exc_info()
            z = (traceback.format_tb(z))
            await err_message.send(z)
            await err_message.send(y)
        except Exception:
            err_message = client.get_user(797387782766592020)
            x, y, z = sys.exc_info()
            z = (traceback.format_tb(z))
            print(y)
            print(z)
            await err_message.send('error too long to send through discord; please check Heroku')


# print(all_coin[-1])
nowtime = datetime.datetime.now()
beforetime = (list(all_coin[-1].values()))[-1]
form = "%Y-%m-%d %H:%M:%S.%f"
beforetime = datetime.datetime.strptime(beforetime, form)
print(nowtime)
print(beforetime)
difference = nowtime - beforetime
print(difference.seconds)
if difference.seconds > 10800:
    for newitem in all_coin:
        new_time = crypttrack.direct_coin_request(newitem["token"], newitem["Name"])
        newitem.update({new_time: nowtime})
        update_coin_text(newitem)

# print(f'the current time is {nowtime}')
delta1 = datetime.timedelta(minutes=nowtime.minute)
delta2 = datetime.timedelta(minutes=60)
deltat = delta2 - delta1
deltat = deltat / datetime.timedelta(minutes=1)
print(f'hourly timer starts in {deltat} minutes')


def decimal_str(y, decimals=15):
    return format(y, f".{decimals}f").lstrip().rstrip('0')


global pseudo_tick_start
pseudo_tick_start = False

task_loop = True
dict_prices = {}
prev_mess = []


def pull_main_token(item, st, dp):
    try:
        new_price = round(crypttrack.direct_coin_request(item['token'], item["Name"]), 15)
    except TypeError:
        print('error, did not pull actual value')
        time.sleep(1)
        new_price = round(crypttrack.direct_coin_request(item['token'], item["Name"]), 15)

    st = st + f'**{item["Name"]}:** *${decimal_str(new_price)}*\n'
    dp.update({item["Name"]: new_price})
    return st


def pull_current_token(item, temp_str, dp, lp):
    try:
        new_price = round(crypttrack.direct_coin_request(item['token'], item["Name"]), 15)
    except TypeError:
        print('error: failed to pull actual value')
        time.sleep(1)
        new_price = round(crypttrack.direct_coin_request(item['token'], item["Name"]), 15)
    try:
        percent = round(crypttrack.ticker_percent(new_price, float(list(item.keys())[-1])), 2)
    except Exception:
        percent = round(crypttrack.ticker_percent(new_price, 0), 2)
    temp_str = temp_str + f'**{item["Name"]}**  **|**  ${decimal_str(new_price)}   **|**  **1h:** *({percent}%*)'
    if len(item) > 26:
        try:
            daily = round(crypttrack.ticker_percent(new_price, float(list(item.keys())[-24])), 2)
            temp_str = temp_str + f'  **|**  **24h:** *({daily}%)*'
        except Exception as err:
            print('something went wrong with daily percent ticker!')
            print(repr(err))
            daily = 0.0
            temp_str = temp_str + f'  **|**  **24h:** *({daily}%)*'
    else:
        daily = 0.0
        temp_str = temp_str + f'  **|**  **24h:** *({daily}%)*'
    lp.add(temp_str)
    dp.update({item["Name"]: new_price})


@tasks.loop(seconds=15)
async def pseudo_ticker():
    global pseudo_tick_start, task_loop, prev_mess, dict_prices
    print(task_loop)
    if pseudo_tick_start is False:
        await client.wait_until_ready()
        pseudo_tick_start = True
    else:
        if task_loop:
            try:
                task_loop = False
                await client.wait_until_ready()
                loop = asyncio.get_event_loop()
                executor = concurrent.futures.ThreadPoolExecutor()
                print('running ticker...')
                string = ''
                temp_str = ''
                dict_prices = {}
                list_prices = set()
                loop_list = []
                start_time = time.time()
                for item in all_coin:
                    if item["Name"] == "BTC" or item["Name"] == 'ETH' or item["Name"] == "ADA" or item["Name"] == "RLC":
                        loop_list.append(loop.run_in_executor(executor, pull_main_token, item, string, dict_prices))
                string = ''.join(await asyncio.gather(*loop_list))
                bnb = round(crypttrack.get_BNB_price() / pow(10, 18), 15)
                string = string + f'**BNB:** *${bnb}*\n\n'
                loop_list = []
                for item in all_coin:
                    if item["Name"] == "BTC" or item["Name"] == 'ETH' or item["Name"] == "ADA" or item["Name"] == "RLC":
                        continue
                    loop_list.append(
                        loop.run_in_executor(executor, pull_current_token, item, temp_str, dict_prices, list_prices))
                await asyncio.gather(*loop_list)
                tt = time.time() - start_time
                print(f'total time: {tt}')

                def sort(e):
                    e = e.split('24h:** *(')[1].split('%)*')[0]
                    return float(e)

                sorted_list = sorted(list_prices, key=sort, reverse=True)
                for item in sorted_list:
                    if item == sorted_list[-1]:
                        string = f'{string} {item}\n'
                        continue
                    string = f'{string} {item}\n split '
                await client.wait_until_ready()
                channel = client.get_channel(833260021642690590)
                async for message in channel.history(limit=200):
                    await message.delete()
                channel = client.get_channel(833260021642690590)
                messages = crypttrack.ticker_mess(string)
                for item in messages:
                    await channel.send(''.join(item))
                print('ticker done')
            except Exception:
                try:
                    err_message = client.get_user(797387782766592020)
                    x, y, z = sys.exc_info()
                    z = (traceback.format_tb(z))
                    await err_message.send(z)
                    await err_message.send(y)
                except Exception:
                    err_message = client.get_user(797387782766592020)
                    x, y, z = sys.exc_info()
                    z = (traceback.format_tb(z))
                    print(y)
                    print(z)
                    await err_message.send('error too long to send through discord; please check Heroku')
        else:
            task_loop = True
            try:
                ntime = datetime.datetime.now()
                pbeforetime = str((list(all_coin[-1].values()))[-1])
                nform = "%Y-%m-%d %H:%M:%S.%f"
                nbeforetime = datetime.datetime.strptime(str(pbeforetime), str(nform))
                print(ntime)
                print(nbeforetime)
                ndifference = ntime - nbeforetime
                print(ndifference.seconds)
                if ndifference.seconds > 10800:
                    for new_item in all_coin:
                        nenwtime = crypttrack.direct_coin_request(new_item["token"], new_item["Name"])
                        new_item.update({nenwtime: ntime})
                        update_coin_text(new_item)
                print('checking flags...')
                print(len(dict_prices))
                print(len(all_coin))
                if len(dict_prices) == len(all_coin):
                    await crypttrack.check_flags(client, flag_list_percent, flag_list_percent_text, dict_prices)
                    print('flag check done!')
                else:
                    mess = client.get_user(797387782766592020)
                    await mess.send(
                        'your suspicions were true; length of dictionary prices did not match the length of coin archive!')
            except Exception:
                try:
                    err_message = client.get_user(797387782766592020)
                    x, y, z = sys.exc_info()
                    z = (traceback.format_tb(z))
                    await err_message.send(z)
                    await err_message.send(y)
                except Exception:
                    err_message = client.get_user(797387782766592020)
                    x, y, z = sys.exc_info()
                    z = (traceback.format_tb(z))
                    print(y)
                    print(z)
                    await err_message.send('error too long to send through discord; please check Heroku')


pseudo_ticker.start()
global bhc_start
bhc_start = True


@tasks.loop(minutes=deltat, count=2)
async def begin_hourly_check():
    global bhc_start
    if bhc_start:
        bhc_start = False
    else:
        print('starting hourly check...')
        hourly_check.start()


@begin_hourly_check.after_loop
async def after_begin_hourly_check():
    print('hourly check started!')


begin_hourly_check.start()


# noinspection PyTypeChecker,PyBroadException
@tasks.loop(hours=1)
async def hourly_check():
    try:
        await client.wait_until_ready()
        current_time = datetime.datetime.today()
        print(f'current hour is: {current_time}')
        for item in all_coin:
            new = crypttrack.direct_coin_request(item["token"], item["Name"])
            item.update({new: current_time})
            update_coin_text(item)
        for item in all_coin:
            if current_time.day == 1 and current_time.hour == 10:
                mpc, new, old, perc = crypttrack.percent_check_monthly(item, 15)
                if mpc:
                    if perc > 0:
                        channel_message = client.get_channel(830985148207202324)
                        await channel_message.send(
                            f'@everyone\nValue of {item["Name"]} increased over 15% in the past month:\n**OLD: **{old}\n**NEW**: {new}\n*({perc})%*')
                    if perc < 0:
                        channel_message = client.get_channel(830654217081454673)
                        await channel_message.send(
                            f'@everyone\nValue of {item["Name"]} decreased over 15% in the past month:\n**OLD: **{old}\n**NEW**: {new}\n*({perc})%*')
                    continue
            if current_time.weekday() == 0 and current_time.hour == 10:
                wpc, new, old, perc = crypttrack.percent_check_weekly(item, 15)
                if wpc:
                    if perc > 0:
                        channel_message = client.get_channel(830985148207202324)
                        await channel_message.send(
                            f'@everyone\nValue of {item["Name"]} increased over 15% in the past week:\n**OLD: **{decimal_str(old)}\n**NEW**: {decimal_str(new)}\n*({perc})%*')
                    if perc < 0:
                        channel_message = client.get_channel(830654217081454673)
                        await channel_message.send(
                            f'@everyone\nValue of {item["Name"]} decreased over 15% in the past week:\n**OLD: **{decimal_str(old)}\n**NEW**: {decimal_str(new)}\n*({perc})%*')
                    continue
            if current_time.hour == 10:
                dpc, new, old, perc = crypttrack.percent_check_daily(item, 15)
                if dpc:
                    if perc > 0:
                        channel_message = client.get_channel(830985148207202324)
                        await channel_message.send(
                            f'@everyone\nValue of {item["Name"]} increased over 15% over the past 24 hours:\n**OLD: **{decimal_str(old)}\n**NEW**: {decimal_str(new)}\n*({perc})%*')
                    if perc < 0:
                        channel_message = client.get_channel(830654217081454673)
                        await channel_message.send(
                            f'@everyone\nValue of {item["Name"]} decreased over 15% over the past 24 hours:\n**OLD: **{decimal_str(old)}\n**NEW**:{decimal_str(new)}\n*({perc})%*')
                    continue
            if current_time.hour == 8 or current_time.hour == 14 or current_time.hour == 20 or current_time.hour == 2:
                qpc, new, old, perc = crypttrack.percent_check_quarterly(item, 20)
                if qpc:
                    if perc > 0:
                        channel_message = client.get_channel(830985148207202324)
                        await channel_message.send(
                            f'@everyone\nValue of {item["Name"]} increased over 20% over the past 6 hours:\n**OLD: **{decimal_str(old)}\n**NEW**: {decimal_str(new)}\n*({perc})%*')
                    if perc < 0:
                        channel_message = client.get_channel(830654217081454673)
                        await channel_message.send(
                            f'@everyone\nValue of {item["Name"]} decreased over 20% over the past 6 hours:\n**OLD: **{decimal_str(old)}\n**NEW**:{decimal_str(new)}\n*({perc})%*')
                    continue
            hpc, new, old, perc = crypttrack.percent_check_hourly(item, 25)
            if hpc:
                if perc > 0:
                    channel_message = client.get_channel(830985148207202324)
                    await channel_message.send(
                        f'@everyone\nValue of {item["Name"]} increased over 25% in the past hour:\n**OLD: **{decimal_str(old)}\n**NEW**: {decimal_str(new)}\n*({perc})%*')
                if perc < 0:
                    channel_message = client.get_channel(830654217081454673)
                    await channel_message.send(
                        f'@everyone\nValue of {item["Name"]} decreased over 25% in the past hour:\n**OLD: **{decimal_str(old)}\n**NEW**: {decimal_str(new)}\n*({perc})%*')

    except Exception:
        try:
            err_message = client.get_user(797387782766592020)
            x, y, z = sys.exc_info()
            z = (traceback.format_tb(z))
            await err_message.send(z)
            await err_message.send(y)
        except Exception:
            err_message = client.get_user(797387782766592020)
            x, y, z = sys.exc_info()
            z = (traceback.format_tb(z))
            print(y)
            print(z)
            await err_message.send('error too long to send through discord; please check Heroku')


client_id = '' #DISCORD CLIENT ID HERE
# Run the client

if __name__ == "__main__":
    client.run(client_id)
