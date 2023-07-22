def create_all_questions(cursor):
    with open('commands_for_tables/add_into_questions_table.sql') as f:
        create_questions = f.read()

    cursor.execute(create_questions, [1, 'В каком году Колумб открыл Америку?', '1492', 'HISTORY'])
    cursor.execute(create_questions, [2, 'Сколько лет длилась 100-летняя война?', '116', 'HISTORY'])
    cursor.execute(create_questions, [3, 'Какой древне-греческой богине был посвящен храм Парфенон?', 'Афине',
                                      'HISTORY'])
    cursor.execute(create_questions, [4, 'На скольких холмах был построен древний город Рим?', 'На семи',
                                      'HISTORY'])
    cursor.execute(create_questions, [5, 'Кто нарисовал фреску «Тайная вечеря»?', 'Леонардо да Винчи', 'ART'])
    cursor.execute(create_questions, [6, 'Кто расписал Сикстинскую капеллу?', 'Микеланджело', 'ART'])
    cursor.execute(create_questions, [7, 'Как назывался древний торговый путь, соединявший Восток с Западом?',
                                      'Шелковый путь', 'HISTORY'])
