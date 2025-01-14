
# Определяет, будет ли включён Компактный режим или Режим списка
default persistent.listui = False
# Автоматически возвращает проигрываемую музыку перед открытием медиаплеера.
default persistent.auto_restore_music = True
# Добавляет к треку эффект проявления/затухания, как в PowerAMP или аналогичной программе.
default persistent.fadein = False

image readablePos = DynamicDisplayable(ost_info.music_pos)
image readableDur = DynamicDisplayable(ost_info.music_dur)
image titleName = DynamicDisplayable(ost_info.dynamic_title_text)
image authorName = DynamicDisplayable(ost_info.dynamic_author_text)
image albumName = DynamicDisplayable(ost_info.dynamic_album_text)
image coverArt = DynamicDisplayable(ost_info.refresh_cover_data) 

screen new_music_room():

    style_prefix "music_player"

    tag menu

    default bar_val = AdjustableAudioPositionValue()

    use game_menu(_("OST-проигрыватель")):

        fixed at music_player_transition:

            if not ost_info.get_current_soundtrack():
                vbox:
                    if persistent.listui:
                        xpos 0.35
                    else:
                        xpos 0.3
                        ypos 0.4

                    text _("Ничего не играет."):
                        color "#000"
                        outlines []
                        size 24

                    hbox:
                        xalign 0.5
                        if not persistent.listui:
                            textbutton _("Список музыки"):
                                action [Show("music_list_type"), With(Dissolve(0.25))]

                        textbutton _("Настройки"):
                            action [Show("music_settings"), With(Dissolve(0.25))]

            elif persistent.listui:
                hbox:
                    xpos 0.08
                    yalign -0.25
                    spacing 10

                    add "coverArt" at cover_art_resize(200)

                    vbox:
                        xoffset 20
                        yalign 0.5

                        add "titleName"

                        add "authorName"

                        add "albumName"

                        hbox:
                            yoffset 5
                            spacing 15

                            imagebutton:
                                idle "mod_assets/music_player/backward.png"
                                hover "mod_assets/music_player/backwardHover.png"
                                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(ost_controls.rewind_music)]

                            imagebutton:
                                idle If(ost_controls.pausedState, "mod_assets/music_player/pause.png", "mod_assets/music_player/play.png")
                                hover If(ost_controls.pausedState, "mod_assets/music_player/play.png", "mod_assets/music_player/pause.png")
                                action If(ost_controls.pausedState, Function(ost_controls.play_music), Function(ost_controls.pause_music))

                            imagebutton:
                                idle "mod_assets/music_player/forward.png"
                                hover "mod_assets/music_player/forwardHover.png"
                                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(ost_controls.forward_music)]

                            null width 15

                            imagebutton:
                                idle ConditionSwitch("ost_controls.loopSong", "mod_assets/music_player/replayOn.png", 
                                    "True", "mod_assets/music_player/replay.png")
                                hover "mod_assets/music_player/replayHover.png"
                                action [ToggleVariable("ost_controls.loopSong", False, True)]
                            imagebutton:
                                idle ConditionSwitch("ost_controls.randomSong", "mod_assets/music_player/shuffleOn.png", 
                                    "True", "mod_assets/music_player/shuffle.png")
                                hover "mod_assets/music_player/shuffleHover.png"
                                action [ToggleVariable("ost_controls.randomSong", False, True)]
                            imagebutton:
                                idle "mod_assets/music_player/info.png"
                                hover "mod_assets/music_player/infoHover.png"
                                action [Show("music_info"), With(Dissolve(0.25))]
                            imagebutton:
                                idle "mod_assets/music_player/settings.png"
                                hover "mod_assets/music_player/settingsHover.png"
                                action [Show("music_settings"), With(Dissolve(0.25))]
                            imagebutton:
                                idle "mod_assets/music_player/refreshList.png"
                                hover "mod_assets/music_player/refreshHover.png"
                                action [Function(ost_song_assign.refresh_list)]

                            null width 15

                            imagebutton:
                                idle ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                                    "mod_assets/music_player/volume.png", "True", 
                                    "mod_assets/music_player/volumeOn.png")
                                hover ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                                    "mod_assets/music_player/volumeHover.png", "True", 
                                    "mod_assets/music_player/volumeOnHover.png")
                                action [Function(ost_controls.mute_player)]
                                yoffset -8
                            bar value Preference ("music_player_mixer volume") xsize 100 yoffset 8 xoffset -15

                        vbox:
                            hbox:
                                bar:
                                    style "music_player_list_bar"

                                    value bar_val
                                    hovered bar_val.hovered
                                    unhovered bar_val.unhovered

                            hbox:
                                add "readablePos" 
                                add "readableDur" xpos 550

            else:

                hbox:
                    xpos 0.06
                    yalign 0.25
                    spacing 10

                    add "coverArt" at cover_art_resize(350)

                    vbox:
                        xoffset 20
                        yalign 0.5

                        vbox:
                            xsize 520
                            add "titleName" 

                            add "authorName" 

                            add "albumName" 

                        hbox:
                            yoffset 5
                            spacing 15

                            imagebutton:
                                idle "mod_assets/music_player/backward.png"
                                hover "mod_assets/music_player/backwardHover.png"
                                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(ost_controls.rewind_music)]

                            imagebutton:
                                idle If(ost_controls.pausedState, "mod_assets/music_player/pause.png", "mod_assets/music_player/play.png")
                                hover If(ost_controls.pausedState, "mod_assets/music_player/play.png", "mod_assets/music_player/pause.png")
                                action If(ost_controls.pausedState, Function(ost_controls.play_music), Function(ost_controls.pause_music))

                            imagebutton:
                                idle "mod_assets/music_player/forward.png"
                                hover "mod_assets/music_player/forwardHover.png"
                                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(ost_controls.forward_music)]

                        hbox:
                            xoffset -2
                            yoffset 10
                            spacing 15

                            imagebutton:
                                idle ConditionSwitch("ost_controls.loopSong", "mod_assets/music_player/replayOn.png", 
                                                    "True", "mod_assets/music_player/replay.png")
                                hover "mod_assets/music_player/replayHover.png"
                                action [ToggleVariable("ost_controls.loopSong", False, True)]
                            imagebutton:
                                idle ConditionSwitch("ost_controls.randomSong", "mod_assets/music_player/shuffleOn.png", 
                                                    "True", "mod_assets/music_player/shuffle.png")
                                hover "mod_assets/music_player/shuffleHover.png"
                                action [ToggleVariable("ost_controls.randomSong", False, True)]
                            imagebutton:
                                idle "mod_assets/music_player/info.png"
                                hover "mod_assets/music_player/infoHover.png"
                                action [Show("music_info"), With(Dissolve(0.25))]
                            imagebutton:
                                idle "mod_assets/music_player/musicwindow.png"
                                hover "mod_assets/music_player/musicwindowHover.png"
                                action [Show("music_list_type"), With(Dissolve(0.25))]
                            imagebutton:
                                idle "mod_assets/music_player/settings.png"
                                hover "mod_assets/music_player/settingsHover.png"
                                action [Show("music_settings"), With(Dissolve(0.25))]
                            imagebutton:
                                idle "mod_assets/music_player/refreshList.png"
                                hover "mod_assets/music_player/refreshHover.png"
                                action [Function(ost_song_assign.refresh_list)]

                hbox:
                    xpos 0.04
                    yalign 0.85
                    vbox:
                        hbox:
                            bar:
                                value bar_val
                                hovered bar_val.hovered
                                unhovered bar_val.unhovered

                        hbox:
                            yoffset 5
                            add "readablePos" 
                            add "readableDur" xpos 630

                    imagebutton:
                        idle ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                            "mod_assets/music_player/volume.png", "True", 
                            "mod_assets/music_player/volumeOn.png")
                        hover ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                            "mod_assets/music_player/volumeHover.png", "True", 
                            "mod_assets/music_player/volumeOnHover.png")
                        action [Function(ost_controls.mute_player)]
                        yoffset -16 xoffset 10
                    bar value Preference ("music_player_mixer volume") xsize 100 xoffset 10

            if persistent.listui:
                vpgrid id "mpl" at music_player_transition:
                    rows len(soundtracks)
                    cols 1
                    mousewheel True
                    draggable True

                    xpos 0.03
                    ypos 0.25
                    xsize 950
                    ysize 380
                    spacing 5

                    for st in soundtracks:
                        frame: 
                            xsize 900
                            button:
                                ysize None
                                action If(ost_info.get_current_soundtrack() == st, If(ost_controls.pausedState, Function(ost_controls.play_music), Function(ost_controls.pause_music)), [SetVariable("ost_controls.pausedState", False), Function(ost_info.set_current_soundtrack, st), Play("music_player", st.path, loop=ost_controls.loopSong, fadein=2.0)])
                                hbox:
                                    if ost_info.get_current_soundtrack() == st:
                                        add Transform(If(ost_controls.pausedState, "mod_assets/music_player/music_list_pause.png", "mod_assets/music_player/music_list_play.png"), size=(68, 68))
                                    else:
                                        add Transform(st.cover_art, size=(68, 68))

                                    null width 12

                                    vbox:
                                        xsize 770
                                        text "{b}[st.name]{/b}" style "music_player_list_title_text"
                                        text "[st.author]" style "music_player_list_author_text"
                                        text "[st.album]"  style "music_player_list_author_text"
                                    if st.byteTime:
                                        vbox:
                                            yalign 0.5
                                            xpos -20
                                            text ost_info.convert_time(st.byteTime) style "music_player_list_author_text"

    text "OST-проигрыватель DDLC, вер. [ostVersion]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"

    if not config.developer:
        hbox:
            xalign 0.5 
            yalign 0.98

            python:
                try:
                    renpy.open_file("RPASongMetadata.json")
                    file_found = True
                except: file_found = False

            if not file_found:
                imagebutton:
                    idle "mod_assets/music_player/osterror.png"
                    action Show("dialog", message=_p("""{b}ВНИМАНИЕ{/b}
Файл метаданных в RPA-архиве не был сгенерирован.
Перечень треков в папке {i}track{/i} не будет составлен, если вы соберёте свою модификацию без этого файла.
Установите значение {u}True{/u} для переменной {i}config.developer{/i}, дабы сгенерировать этот файл."""),
                        ok_action=Hide("dialog"))

    # Начать играть музыку при входе в музыкальный зал.
    on "replace" action [Function(ost_main.ost_start), Stop("music", fadeout=1.0)]
    on "show" action [Function(ost_main.ost_start), Stop("music", fadeout=1.0)]

    # Восстанавливать музыку главного меню при выходе.
    on "hide" action [If(persistent.auto_restore_music,
        [Stop("music_player", fadeout=1.0), SetMute("music", False), Play("music", ost_main.prevTrack, fadein=1.0)],
        SetMute("music", True))]
    on "replaced" action [Hide("music_settings"), Hide("music_list"), Hide("music_list_type"), 
        Hide("music_info"), Function(ost_main.ost_log_stop), If(persistent.auto_restore_music,
        [Function(ost_controls.pause_music), SetMute("music", False), Play("music", ost_main.prevTrack, fadein=1.0)],
        SetMute("music", True))]

screen music_list_type(type=None):

    style_prefix "music_window"

    drag:
        drag_name "mlisttype"
        drag_handle (0, 0, 1.0, 40)
        xsize 470
        ysize 260
        xpos 0.3
        ypos 0.2

        frame:

            if type is not None:
                hbox:
                    xalign 0.05 ypos 0.005
                    textbutton "<-":
                        text_style "navigation_button_text"
                        action [Hide("music_list"), Show("music_list_type")]

            hbox:
                ypos 0.005
                xalign 0.52 
                text _("Список музыки")

            hbox:
                ypos 0.005
                xalign 0.98
                textbutton "X":
                    text_style "navigation_button_text"
                    action Hide("music_list_type")

            side "c":
                xpos 0.05
                ypos 0.2
                xsize 430
                ysize 200

                viewport id "mlt":
                    mousewheel True
                    draggable True
                    has vbox

                    if type is None:
                        textbutton _("Все треки"):
                            action [Hide("music_list_type"), Show("music_list")]

                        textbutton _("Исполнитель"):
                            action [Show("music_list_type", type="artist")]

                        textbutton _("Составитель альбома"):
                            action [Show("music_list_type", type="albumartist")]

                        textbutton _("Композитор"):
                            action [Show("music_list_type", type="composer")]

                        textbutton _("Жанр"):
                            action [Show("music_list_type", type="genre")]

                    else:
                        python:
                            temp_list = []
                            for st in soundtracks:
                                if type == "artist":
                                    if st.author not in temp_list:
                                        temp_list.append(st.author)
                                elif type == "albumartist":
                                    if st.albumartist not in temp_list:
                                        temp_list.append(st.albumartist)
                                elif type == "composer":
                                    if st.composer not in temp_list:
                                        temp_list.append(st.composer)
                                elif type == "genre":
                                    if st.genre not in temp_list:
                                        temp_list.append(st.genre)

                            temp_list = sorted(temp_list)

                        for st in temp_list:
                            textbutton "[st]":
                                action [Hide("music_list_type"), Show("music_list", type=type, arg=st)]

    on "hide" action With(Dissolve(0.25))

screen music_list(type=None, arg=None):

    style_prefix "music_window"

    drag:
        drag_name "mlist"
        drag_handle (0, 0, 1.0, 40)
        xsize 470
        ysize 260
        xpos 0.3
        ypos 0.2

        python:
            new_soundtrack_list = []
            for st in soundtracks:
                if type == "artist":
                    if arg == st.author:
                        new_soundtrack_list.append(st)
                elif type == "albumartist":
                    if arg == st.albumartist:
                        new_soundtrack_list.append(st)
                elif type == "composer":
                    if arg == st.composer:
                        new_soundtrack_list.append(st)
                elif type == "genre":
                    if arg == st.genre:
                        new_soundtrack_list.append(st)
                else:
                    new_soundtrack_list.append(st)

            new_soundtrack_list = sorted(new_soundtrack_list, key=lambda new_soundtrack_list: new_soundtrack_list.name)

        frame:
            hbox:
                xalign 0.05 ypos 0.005
                textbutton "<-":
                    text_style "navigation_button_text"
                    action [Hide("music_list"), Show("music_list_type", type=type)]

            hbox:
                ypos 0.005
                xalign 0.52 
                text _("Список музыки")

            hbox:
                ypos 0.005
                xalign 0.98
                textbutton "X":
                    text_style "navigation_button_text"
                    action Hide("music_list")

            side "c":
                xpos 0.05
                ypos 0.2
                xsize 430
                ysize 200

                viewport id "ml":
                    draggable True
                    mousewheel True
                    has vbox

                    for nst in new_soundtrack_list:
                        textbutton "[nst.name]":
                            style "l_list"
                            text_style "music_window_button_text"
                            action [Hide("music_list"), Function(ost_info.set_current_soundtrack, nst), Play("music_player", nst.path, loop=ost_controls.loopSong, fadein=2.0)]

    on "hide" action With(Dissolve(0.25))

screen music_settings():

    style_prefix "music_settings"

    drag:
        drag_name "msettings"
        drag_handle (0, 0, 1.0, 40)
        xsize 470
        ysize 260
        xpos 0.5
        ypos 0.5

        frame:
            hbox:
                ypos 0.005
                xalign 0.52 
                text _("Настройки") style "music_window_text"

            hbox:
                ypos 0.005
                xalign 0.98
                textbutton "X":
                    text_style "navigation_button_text"
                    action Hide("music_settings")

            side "c":
                xpos 0.05
                ypos 0.2
                xsize 430
                ysize 200

                viewport id "mlt":
                    mousewheel True
                    draggable True
                    has vbox

                    label _("Интерфейс")
                    vbox:
                        textbutton _("Компактный режим"):
                            style "radio_button" 
                            action [Hide("music_list_type"), Hide("music_list"), Hide("music_info"),
                                ToggleField(persistent, "listui", False, True)]

                    label _("Проигрыватель")
                    vbox:
                        textbutton _("Возвращать музыку при выходе"):
                            style "radio_button" 
                            action InvertSelected(ToggleField(persistent, "auto_restore_music", False, True))

                        textbutton _("Эффект проявления/затухания"):
                            style "radio_button" 
                            action InvertSelected(ToggleField(persistent, "fadein", False, True))

                    textbutton _("Об OST-проигрывателе DDLC"):
                        text_style "navigation_button_text" 
                        action Show("dialog", message=_p("""OST-проигрыватель DDLC от Азариэль Дель Кармена (bronya_rand).
Авторские права © 2020-наст. вр. Азариэль Дель Кармен (bronya_rand).
Перевод на русский (RG Smoking Room):
Amanda Watson – текстовая и скриптовая составляющие
Inui-senpai – графическая составляющая"""), 
                            ok_action=Hide("dialog"))

    on "hide" action With(Dissolve(0.25))   

screen music_info():

    style_prefix "music_window"

    drag:
        drag_name "minfo"
        drag_handle (0, 0, 1.0, 40)
        xsize 480
        ysize 260
        xpos 0.4
        ypos 0.4

        frame:
            hbox:
                ypos 0.005
                xalign 0.52 
                text _("О треке")

            hbox:
                ypos 0.005
                xalign 0.98
                textbutton "X":
                    text_style "navigation_button_text"
                    action Hide("music_info")

            side "c":
                xpos 0.05
                ypos 0.2
                xsize 460
                ysize 200

                viewport id "mi":
                    mousewheel True
                    draggable True
                    has vbox

                    python:
                        albumartist = ost_info.get_album_artist()
                        composer = ost_info.get_composer()
                        genre = ost_info.get_genre()
                        sideloaded = ost_info.get_sideload()
                        comment = ost_info.get_description() or None

                    text _("{u}Составитель альбома{/u}: [albumartist]") style "music_player_info_text"
                    text _("{u}Композитор{/u}: [composer]") style "music_player_info_text"
                    text _("{u}Жанр{/u}: [genre]") style "music_player_info_text"
                    text _("{u}Предзагрузка{/u}: [sideloaded]") style "music_player_info_text"
                    text _("{u}Комментарий{/u}: [comment]") style "music_player_info_text"

    on "hide" action With(Dissolve(0.25))    
