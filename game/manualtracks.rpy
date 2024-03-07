
init python:    
    ## Параметры ручного определения треков
    #     name - Название трека [ОБЯЗАТЕЛЬНО]
    #     author - Исполнитель трека [ОБЯЗАТЕЛЬНО]
    #     path - Путь к треку [ОБЯЗАТЕЛЬНО]
    #     album - Альбом трека
    #     albumartist - Составитель этого альбома
    #     composer - Композитор трека (человек, который написал музыку к нему)
    #     genre - Жанр трека
    #     description - Описание/комментарий трека
    #     cover_art - Путь к обложке трека или 'False'
    #                 (без кавычек), если у этого трека нет обложки [ОБЯЗАТЕЛЬНО]
    #     unlocked = 'True' (без кавычек) для мгновенной разблокировки или
    #                условие renpy.seen_audio("путь/к/треку.формат"), от которого
    #                и будет зависеть разблокировка

    your_reality = soundtrack(
        name = __("Твоя реальность"),
        author = __("Моника"),
        path = "bgm/credits.ogg",
        description = __("Я натворила делов, сделала тебе больно, сделала больно своим друзьям. Я могу лишь надеяться на то, что вы все простите меня."),
        cover_art = False
    )     
    manualDefineList.append(your_reality)

    Wake_Up_Unchanged = soundtrack(
        name = __("Неизменный"),
        path = "mod_assets/music_player/sample/Unchanged.ogg",
        author = "PabloLuaxerc#1719",
        description = __("Грустный саундтрек"),
        cover_art = "mod_assets/music_player/sample/cover.png"
    )
    manualDefineList.append(Wake_Up_Unchanged)

    ## Пример

    # poem_panic = soundtrack(
    #     name = __("Стихотворный замес"),
    #     path = "bgm/example.ogg",
    #     author = __("Дэн Салвато"),
    #     description = __("Пример"),
    #     unlocked = renpy.seen_audio("bgm/example.ogg")
    # )
    # manualDefineList.append(poem_panic)
