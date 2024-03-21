from ds_messenger import DirectMessenger

new_profile = DirectMessenger('168.235.86.101', "ishantrivedi", "ilovemia")
new_profile.send("yo", "kia")
new_profile.close_sock()