
# Основано на ost.py из Renpy-Universal-Player

init python:
    import re
    import io
    import os
    import pygame_sdl2
    import logging
    import json
    import threading
    from tinytag import TinyTag

    enable_logging = False

    renpy.store.build.archive("track", "mod")
    renpy.store.build.classify("game/RPASongMetadata.json", "track all")
    renpy.store.build.classify("game/python-packages/binaries.txt", "mod all")
    renpy.store.build.classify("game/python-packages/tinytag.py", "mod all")
    renpy.store.build.classify("game/track/**", "track all")

    # Создание музыкальной комнаты и инициализация кода
    ostVersion = 3.21
    renpy.audio.music.register_channel("music_player", mixer="music_player_mixer", loop=False)

    gamedir = os.environ["ANDROID_PUBLIC"] if renpy.android else renpy.config.gamedir.replace("\\", "/")

    # Списки для хранения аудиозаписей
    soundtracks = []

    renpy.random.Random()

    class OSTPlayerInfo():
        def __init__(self, channel="music_player"):
            self.current_soundtrack = None
            self.channel = channel
            self.time_position = 0.0
            self.time_duration = 1.0

        def get_pos(self):
            if renpy.audio.music.get_pos(self.channel) is not None:
                self.time_position = renpy.audio.music.get_pos(self.channel)

            return self.time_position

        def get_duration(self, songPath=None):
            if self.current_soundtrack and self.get_bytetime() and not songPath:
                return self.get_bytetime()
            else:
                try:
                    pathToSong = songPath if songPath else self.get_path()

                    tags = TinyTag.get(pathToSong, image=False)

                    if tags.duration:
                        self.time_duration = tags.duration
                    else:
                        if not songPath:
                            self.time_duration = renpy.audio.music.get_duration(self.channel) or self.time_duration

                except:
                    if not songPath:
                        self.time_duration = renpy.audio.music.get_duration(self.channel) or self.time_duration

            return self.time_duration

        def convert_time(self, x):
            hour = ""

            if int (x / 3600) > 0:
                hour = f"{int(x / 3600)}"

            if hour != "":
                if int((x % 3600) / 60) < 10:
                    minute = f":0{int((x % 3600) / 60)}"
                else:
                    minute = f":{int((x % 3600) / 60)}"
            else:
                minute = f"{int(x / 60)}"

            if int(x % 60) < 10:
                second = f":0{int(x % 60)}"
            else:
                second = f":{int(x % 60)}"

            return f"{hour}{minute}{second}"

        def set_current_soundtrack(self, nst):
            self.current_soundtrack = nst

        def get_current_soundtrack(self):
            return self.current_soundtrack

        def get_title(self):
            return self.current_soundtrack.name

        def get_artist(self):
            return self.current_soundtrack.author

        def get_album(self):
            return self.current_soundtrack.album

        def get_album_artist(self):
            return self.current_soundtrack.albumartist

        def get_composer(self):
            return self.current_soundtrack.composer

        def get_genre(self):
            return self.current_soundtrack.genre

        def get_bytetime(self):
            return self.current_soundtrack.byteTime

        def get_sideload(self):
            return self.current_soundtrack.sideloaded

        def get_description(self):
            return self.current_soundtrack.description

        def get_cover_art(self):
            return self.current_soundtrack.cover_art

        def get_path(self):
            return self.current_soundtrack.path

        def music_pos(self, st, at):
            readableTime = self.convert_time(self.get_pos())

            if persistent.listui: return renpy.text.text.Text(readableTime,
                style="song_progress_text", size=16), 0.20
            return renpy.text.text.Text(readableTime, style="song_progress_text"), 0.20

        def music_dur(self, st, at):
            readableDuration = self.convert_time(self.get_duration()) 

            if persistent.listui: return renpy.text.text.Text(readableDuration, 
                style="song_duration_text", size=16), 0.20
            return renpy.text.text.Text(readableDuration, style="song_duration_text"), 0.20

        def dynamic_title_text(self, st, at):
            if persistent.listui:
                return renpy.text.text.Text(
                    (
                        f"{self.get_title()[:52]}..."
                        if len(self.get_title()) >= 55
                        else self.get_title()
                    ), style="music_player_label_text", substitute=False, 
                    size=20
                ), 0.20

            return renpy.text.text.Text(
                (
                    f"{self.get_title()[:47]}..."
                    if len(self.get_title()) >= 50
                    else self.get_title()
                ), style="music_player_label_text", substitute=False
            ), 0.20

        def dynamic_author_text(self, st, at):
            if persistent.listui:
                return renpy.text.text.Text(
                    (
                        f"{self.get_artist()[:62]}..."
                        if len(self.get_artist()) >= 65
                        else self.get_artist()
                    ), style="music_player_text", substitute=False, 
                    size=20
                ), 0.20

            return renpy.text.text.Text(
                (
                    f"{self.get_artist()[:42]}..."
                    if len(self.get_artist()) >= 45
                    else self.get_artist()
                ), style="music_player_text", substitute=False
            ), 0.20

        def refresh_cover_data(self, st, at):
            return renpy.display.im.image(self.get_cover_art()), 0.20

        def dynamic_album_text(self, st, at):
            if persistent.listui:
                return renpy.text.text.Text(
                    (
                        f"{self.get_album()[:62]}..."
                        if len(self.get_album()) >= 65
                        else self.get_album()
                    ), style="music_player_text", substitute=False, 
                    size=20
                ), 0.20

            return renpy.text.text.Text(
                (
                    f"{self.get_album()[:42]}..."
                    if len(self.get_album()) >= 45
                    else self.get_album()
                ), style="music_player_text", substitute=False
            ), 0.20

    ost_info = OSTPlayerInfo()

    class OSTPlayerControls():
        def __init__(self, channel="music_player"):
            self.channel = channel
            self.pausedState = False
            self.pausedAt = None
            self.oldVolume = 0.0
            self.randomSong = False
            self.loopSong = False

        def get_loop_status(self):
            return self.loopSong

        def get_shuffle_status(self):
            return self.randomSong

        def pause_music(self):
            if not renpy.audio.music.is_playing(self.channel):
                return

            self.pausedState = True

            soundtrack_position = (renpy.audio.music.get_pos(self.channel) or 0.0) + (1.6 if persistent.fadein else 0.0)

            if soundtrack_position is not None:
                self.pausedAt = f"<from {soundtrack_position}>{ost_info.get_path()}"

            renpy.audio.music.stop(self.channel, fadeout=(2.0 if persistent.fadein else 0.0))

        def play_music(self):
            self.pausedState = False

            if not self.pausedAt:
                renpy.audio.music.play(ost_info.get_path(), self.channel, fadein=(2.0 if persistent.fadein else 0.0))
            else:
                renpy.audio.music.play(self.pausedAt, self.channel, fadein=(2.0 if persistent.fadein else 0.0))

        def forward_music(self):
            if not renpy.audio.music.get_pos(self.channel):
                soundtrack_position = ost_info.get_pos() + 5
            else:
                soundtrack_position = renpy.audio.music.get_pos(self.channel) + 5

            if soundtrack_position >= ost_info.get_duration():
                self.pausedAt = False
                if self.randomSong:
                    self.random_song()
                else:
                    self.next_track()
            else:
                self.pausedAt = f"<from {soundtrack_position}>{ost_info.get_path()}"

                renpy.audio.music.play(self.pausedAt, self.channel)

        def rewind_music(self):
            if not renpy.audio.music.get_pos(self.channel):
                soundtrack_position = ost_info.get_pos() - 5
            else:
                soundtrack_position = renpy.audio.music.get_pos(self.channel) - 5

            if soundtrack_position <= 0.0:
                self.pausedAt = False
                self.next_track(True)
            else:
                self.pausedAt = f"<from {soundtrack_position}>{ost_info.get_path()}"

                renpy.audio.music.play(self.pausedAt, self.channel)

        def next_track(self, back=False):
            index = 0
            while ost_info.current_soundtrack != soundtracks[index]:
                index = index + 1

            if back:
                ost_info.current_soundtrack = soundtracks[index-1]
            else:
                try: ost_info.current_soundtrack = soundtracks[index+1]
                except: ost_info.current_soundtrack = soundtracks[0]

            if not renpy.get_screen("new_music_room"):
                renpy.notify(f"Сейчас играет: {ost_info.get_title()} – {ost_info.get_artist()}")

            renpy.audio.music.play(ost_info.get_path(), self.channel, self.loopSong)

        def random_track(self):
            unique = 1
            while unique != 0:
                a = renpy.random.randint(0, len(soundtracks))
                if ost_info.current_soundtrack != soundtracks[a]:
                    unique = 0
                    ost_info.current_soundtrack = soundtracks[a]

            if not renpy.get_screen("new_music_room"):
                renpy.notify(f"Сейчас играет: {ost_info.get_title()} – {ost_info.get_artist()}")

            renpy.audio.music.play(ost_info.get_path(), self.channel, self.loopSong)

        def mute_player(self):
            logging.info("Заглушаю медиаплеер.")

            if renpy.game.preferences.get_volume("music_player_mixer") != 0.0:
                self.oldVolume = renpy.game.preferences.get_volume("music_player_mixer")
                renpy.game.preferences.set_volume("music_player_mixer", 0.0)
            else:
                if self.oldVolume == 0.0:
                    renpy.game.preferences.set_volume("music_player_mixer", 0.5)
                else:
                    renpy.game.preferences.set_volume("music_player_mixer", self.oldVolume)

        def check_paused_state(self):
            logging.info("Проверяю, существует ли сессия музыки или мы сейчас на паузе.")
            if not ost_info.current_soundtrack or self.pausedState:
                logging.info("Сессия музыки не найдена, либо мы сейчас на паузе. Выхожу из стадии проверки.")
                return
            else:
                logging.info("Сессия музыки была найдена, либо мы сейчас не на паузе. Останавливаю сессию музыки и выхожу из стадии проверки.")
                self.pause_music()

    ost_controls = OSTPlayerControls()

    class soundtrack:
        def __init__(self, name, author, path, album="Неизвестный альбом", albumartist="Неизвестный составитель альбома", 
            composer="Неизвестный композитор", genre="Неизвестный жанр", byteTime=False, 
            sideloaded=False, description="", cover_art=None, unlocked=True):
            self.name = name
            self.author = author
            self.path = path
            self.album = album
            self.albumartist = albumartist
            self.composer = composer
            self.genre = genre
            self.byteTime = byteTime
            self.sideloaded = sideloaded
            self.description = description
            if not cover_art:
                self.cover_art = "mod_assets/music_player/nocover.png"
            else:
                self.cover_art = cover_art
            self.unlocked = unlocked

    class ExternalOSTMonitor:
        def __init__(self, channel="music_player"):
            self.channel = channel
            self.periodic_condition = threading.Condition()
            self.t1 = threading.Thread(target=self.periodic, daemon=True)
            self.t1.start()

        def get_pos_duration(self):
            pos = renpy.audio.music.get_pos(self.channel) or 0.0
            duration = ost_info.get_duration()

            return pos, duration

        def get_song_options_status(self):
            return ost_controls.loopSong, ost_controls.randomSong

        def periodic(self):
            while True:
                with self.periodic_condition:
                    self.periodic_condition.wait(.05)

                pos, duration = self.get_pos_duration()
                loopThis, doRandom = self.get_song_options_status()

                if pos >= duration - 0.20:
                    if loopThis:
                        renpy.audio.music.play(ost_info.get_path(), self.channel, 
                            loop=True)
                    elif doRandom:
                        ost_controls.random_track()
                    else:
                        ost_controls.next_track() 

    @renpy.exports.pure
    class AdjustableAudioPositionValue(renpy.ui.BarValue):
        def __init__(self, channel='music_player', update_interval=0.0):
            self.channel = channel
            self.update_interval = update_interval
            self.adjustment = None
            self._hovered = False

        def get_pos_duration(self):
            pos = renpy.audio.music.get_pos(self.channel) or 0.0
            duration = ost_info.get_duration()

            return pos, duration

        def get_adjustment(self):
            pos, duration = self.get_pos_duration()
            self.adjustment = renpy.ui.adjustment(value=pos, range=duration, 
                                                changed=self.set_pos, adjustable=True)

            return self.adjustment

        def hovered(self):
            self._hovered = True

        def unhovered(self):
            self._hovered = False

        def set_pos(self, value):
            if (self._hovered and pygame_sdl2.mouse.get_pressed()[0]):
                if ost_controls.pausedState: ost_controls.pausedState = False
                renpy.audio.music.play(f"<from {value}>{ost_info.get_path()}",
                    self.channel)
                if ost_controls.loopSong:
                    renpy.audio.music.queue(ost_info.get_path(), self.channel, True)

        def periodic(self, st):

            pos, duration = self.get_pos_duration()

            if pos and pos <= duration:
                self.adjustment.set_range(duration)
                self.adjustment.change(pos)

            return self.update_interval 

    class OSTPlayerSongAssign():
        def __init__(self):
            self.automaticList = []
            self.manualList = []
            self.file_types = ('.mp3', '.ogg', '.opus', '.wav')

        def refresh_list(self):
            logging.info("Обновляю список медиаплеера.")
            self.scan_song()
            if renpy.config.developer:
                self.rpa_mapping()
            self.resort()

        def resort(self):
            global soundtracks
            logging.info("Сортирую список медиаплеера.")

            for obj in self.automaticList:
                if obj not in soundtracks and obj.unlocked:
                    soundtracks.append(obj)
            logging.info("Найденные песни были добавлены в список медиаплеера.")

            for obj in self.manualList:
                if obj not in soundtracks and obj.unlocked:
                    soundtracks.append(obj)
            logging.info("Прописанные вручную песни были добавлены в список медиаплеера.")

            soundtracks = sorted(soundtracks, key=lambda soundtracks: soundtracks.name)

        def get_info(self, path, tags):
            sec = tags.duration
            try:
                image_data = tags.get_image()

                if image_data is None:
                    return None

                with renpy.exports.file("python-packages/binaries.txt") as a:
                    lines = a.readlines()

                for line in image_data.splitlines():
                    if b"PNG" in line:
                        cover_formats = ".png"
                        line.replace(line, lines[2])
                    elif b"JFIF" in line:
                        cover_formats = ".jpg"
                        line.replace(line, lines[1])
                    break

                if cover_formats is None:
                    raise UnknownImageFileType

                coverAlbum = re.sub(r"(\\|/|\:|\?|\*|\<|\>|\||\[|\])", "", tags.album or tags.title)

                if not os.path.exists(os.path.join(gamedir, 'track/covers', f"{coverAlbum}{cover_formats}")):

                    with open(os.path.join(gamedir, 'track/covers', f"{coverAlbum}{cover_formats}"), 'wb') as f:
                        f.write(image_data)

                art = f"track/covers/{coverAlbum}{cover_formats}"
                logging.info(f"Получена обложка альбома для трека {path}.")
                return art
            except UnknownImageFileType:
                logging.warning("Не удалось найти/сохранить обложку альбома в каталоге \"covers\".")
                return None
            except:
                raise

        def scan_song(self):
            logging.info("Сканирую каталоги с музыкой.")
            exists = self.check_removed_songs()

            logging.info("Сканирую каталог \"track\" на наличие музыки.")
            for x in os.listdir(f"{gamedir}/track"):
                if x.endswith((self.file_types)) and f"track/{x}" not in exists:
                    path = f"track/{x}"
                    logging.info(f"Получение метаданных для трека {path}.")

                    try: tags = TinyTag.get(f"{gamedir}/{path}", image=True)
                    except IOError: 
                        logging.error(f"При попытке получения метаданных для трека {path} возникло исключение \"IOError\". Пропускаю трек.")
                        continue

                    albumart = self.get_info(path, tags)
                    self.def_song(path, tags, albumart, True)
                    exists.append(path)

        def check_removed_songs(self):
            exists = []
            logging.info("Проверяю наличие удалённых треков.")

            for x in self.automaticList[:]:
                renpy.exports.file(x.path)
                exists.append(x.path)
                logging.info(f"Трек {x.path} был удалён из списка медиаплеера.")
                self.automaticList.remove(x)

            return exists

        def def_song(self, path, tags, albumart, unlocked=True):
            logging.info(f"Определение треков, расположенных в {path}, для медиаплеера.")            

            class_name = re.sub(r"-|'| ", "_", tags.title or str(path.replace("track/", "")))

            class_name = soundtrack(
                name = tags.title or str(path.replace("track/", "")),
                author = tags.artist or "Неизвестный исполнитель",
                album = tags.album or "Неизвестный альбом",
                albumartist = tags.albumartist or "Неизвестный составитель альбома",
                composer = tags.composer or "Неизвестный композитор",
                genre = tags.genre or "Неизвестный жанр",
                path = path,
                byteTime = tags.duration or False,
                sideloaded = True,
                description = tags.comment or "",
                cover_art = albumart,
                unlocked = unlocked
            )
            self.automaticList.append(class_name)

        def rpa_mapping(self):
            if not renpy.config.developer: return
            data = []

            try: os.remove(os.path.join(gamedir, "RPASongMetadata.json"))
            except: pass

            for y in self.automaticList:
                data.append ({
                    "class": re.sub(r"-|'| ", "_", y.name or str(y.path.replace("track/", ""))),
                    "title": y.name,
                    "artist": y.author,
                    "album": y.album,
                    "albumartist": y.albumartist,
                    "composer": y.composer,
                    "genre": y.genre,
                    "path": y.path,
                    "sec": y.byteTime,
                    "sideloaded": y.sideloaded,
                    "comment": y.description,
                    "cover_art": y.cover_art,
                    "unlocked": y.unlocked,
                })

            with open(f"{gamedir}/RPASongMetadata.json", "a") as f:
                json.dump(data, f)

        def rpa_load_mapping(self):
            try: 
                logging.info(f"Попытка загрузить файл \"RPASongMetadata.json\".")
                with renpy.exports.file("RPASongMetadata.json") as f:
                    data = json.load(f)
                logging.info("Файл \"RPASongMetadata.json\" загружен.")
            except IOError: 
                logging.warning("Ошибка загрузки файла \"RPASongMetadata.json\".")
                return

            exists = self.check_removed_songs()

            for p in data:
                logging.info(f"Определение кэшированного класса {p['class']} для медиаплеера.")
                if p['path'] not in exists:

                    p['class'] = soundtrack(
                        name = p['title'],
                        author = p['artist'],
                        album = p['album'],
                        albumartist = p['albumartist'],
                        composer = p['composer'],
                        genre = p['genre'],
                        path = p['path'],
                        byteTime = p['sec'],
                        sideloaded = p['sideloaded'],
                        description = p['comment'],
                        cover_art = p['cover_art'],
                        unlocked = p['unlocked']
                    )
                    self.automaticList.append(p['class'])

    ost_song_assign = OSTPlayerSongAssign()

    class OSTPlayerMain():
        def __init__(self):
            self.prevTrack = None

            self.logdir = f"{os.environ['ANDROID_PUBLIC'] if renpy.android else config.basedir}/ost_log.txt"

            if enable_logging:
                if renpy.get_autoreload():
                    self.ost_log_stop()

                if os.path.exists(self.logdir):
                    os.remove(self.logdir)

                self.ost_log_start()

            logging.info(f"Создаю папку \"track\" в {gamedir}, если оная отсутствует.")
            try: os.mkdir(os.path.join(gamedir, "track"))
            except: pass
            logging.info(f"Создаю папку \"covers\" в {gamedir}/track, если оная отсутствует.")
            try: os.mkdir(os.path.join(gamedir, "track", "covers"))
            except: pass

            logging.info("Очистка папки \"covers\" от имеющихся обложек.")
            for x in os.listdir(os.path.join(gamedir, "track", "covers")):
                os.remove(os.path.join(gamedir, "track", "covers", x))

            ost_song_assign.scan_song()

        def get_music_channel_info(self):
            logging.info("Узнаю, какая сейчас музыка играет на соответствующем аудио-канале.")
            self.prevTrack = renpy.audio.music.get_playing(channel='music') or self.prevTrack
            logging.info("Статус музыки получен от \"renpy.audio.music\".")

            if not self.prevTrack:
                logging.warning("На \"renpy.audio.music\" не было найдено никакой музыки.")
                self.prevTrack = False

        def ost_log_start(self):
            logging.basicConfig(filename=self.logdir, level=logging.DEBUG)
            logging.info("Начало логирования сессии OST-проигрывателя для ошибок.")

        def ost_log_stop(self):
            logging.info("Останов логирования сессии OST-проигрывателя для ошибок.")
            logging.shutdown()

        def ost_start(self):
            if renpy.config.developer: ost_song_assign.rpa_mapping()
            else: ost_song_assign.rpa_load_mapping() 
            self.get_music_channel_info()
            ost_song_assign.resort()

        def ost_quit(self):
            ost_controls.check_paused_state()
            if enable_logging: self.ost_log_stop()

    ost_main = OSTPlayerMain()
    renpy.game.preferences.set_mute("music", False)
    ost_monitor = ExternalOSTMonitor()

    # Обратная совместимость
    manualDefineList = ost_song_assign.manualList