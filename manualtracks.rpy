
init python:    
    ### Template for Manual Soundtracks
    # This method still works however now you must include manualDefineList.append(variable) 
    # to add it properly for refreshing.
    # priority has been depreciated in favor for 'sideloaded'.

    your_reality = soundtrack(
        name = "Your reality",
        author = "Monika",
        path = "bgm/credits.ogg",
        description = "I made mistakes, hurt you, hurt my friends. All I can do is hope you all forgive me.",
        cover_art = False
    )     
    manualDefineList.append(your_reality)
    
    Wake_Up_Unchanged = soundtrack(
        name = "Unchanged",
        path = "mod_assets/music_player/sample/Unchanged.ogg",
        author = "PabloLuaxerc#1719",
        description = "Sad soundtrack",
        cover_art = "mod_assets/music_player/sample/cover.png"
    )
    manualDefineList.append(Wake_Up_Unchanged)

    # poem_panic = soundtrack(
    #     name = "Poem Panic",
    #     path = "bgm/example.ogg",
    #     author = "Dan Salvato",
    #     description = "Example",
    #     unlocked = renpy.seen_audio("bgm/example.ogg")
    # )
    # manualDefineList.append(poem_panic)