import json
import datetime
usr_dict = dict()
tag_dict = dict()
col_dict = dict()
events = list()
event_tag = ""
days_list = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье", "Выполнено"]

date_field = "ДАТА"
org_field = "ОТВЕТСТВЕННЫЙ (кто будет)"
name_field = "СОБЫТИЕ"
post_field = "ПОСТ (ссылка)"
post_date_field = "ПОСТ (дата dd.mm и день недели)"
post_time_field = "ПОСТ (время)"
num_field = "КОЛ-ВО УЧАСТНИКОВ"
place_field = "МЕСТО (корпус, ауд.N)"
time_start_field = "ВРЕМЯ НАЧАЛА"
time_finish_field = "ВРЕМЯ КОНЦА"
event_label = "event"


def get_users(res):
    for usr_data in res['members']:
        usr_dict[usr_data['id']] = usr_data['fullName']


def get_tags(res):
    ev_tag = ""
    for tag_data in res['labels']:
        if tag_data['name'] and tag_data['name'] == event_label:
            ev_tag = tag_data['id']
        elif tag_data['name']:
            tag_dict[tag_data['id']] = tag_data['name']
    return ev_tag


def get_cols(res):
    for col_data in res['lists']:
        if col_data['name'] in days_list:
            col_dict[col_data['id']] = col_data['name']


def get_cards(res):
    for card in res['cards']:
        if event_tag in card['idLabels']:
            event = dict()
            date_time = datetime.datetime.strptime(card['due'], "%Y-%m-%dT%H:%M:%S.%fZ")
            date_format = "%Y-%m-%d"
            event[date_field] = date_time.strftime(date_format)
            event[org_field] = list()
            for org_id in card['idMembers']:
                event[org_field].append(usr_dict[org_id])
            event[name_field] = card['name']
            event[post_field] = list()
            for link in card['attachments']:
                event[post_field].append(link['url'])
            desc = list(card['desc'].split('\n'))
            event[place_field] = desc[2]
            event[time_start_field] = desc[3].split("-")[0].strip()
            event[time_finish_field] = desc[3].split("-")[1].strip()
            event[post_date_field] = list()
            event[post_time_field] = list()

            for i in range(6, len(desc)):
                if desc[i]:
                    p_date, p_time = desc[i].split(", ")
                    event[post_date_field].append(p_date)
                    event[post_time_field].append(p_time)

            for act in res['actions']:
                if 'text' in act['data']:
                    if act['data']['text'].isdigit():
                        event[num_field] = act['data']['text']

            events.append(event)


def out_pretty(e):
    for d in e:
        for field in d:
            if not isinstance(d[field], list):
                print(field, d[field])
            else:
                print(field, *d[field])
        print()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open("resources.json", "r", encoding="utf-8") as read_file:
        data = json.load(read_file)
    get_users(data)
    #print(usr_dict)
    event_tag = get_tags(data)
    #print(tag_dict)
    get_cols(data)
    #print(col_dict)
    get_cards(data)
    out_pretty(events)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
