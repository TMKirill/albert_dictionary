# Review

This project provides interface for dict.cc based txt dictionaries inside the Albert launcher.

For this to work you need to go to https://my.dict.cc/ and get the dictionaries

# Install

```
git clone https://github.com/TMKirill/albert_dictionary.git  ~/.local/share/albert/python/plugins/dictionary
```
- add .txt file from https://my.dict.cc/ to the ./dictionaries directory, create if you don't have it (I recommend to rename files for better usability)
- restart albert
- turn on the dictionary plugin in albert plugin settings

# Setting

<img width="1594" height="532" alt="image" src="https://github.com/user-attachments/assets/ea9f8adc-4fd0-4676-afa5-de4927e0d6c9" />

You can set the basic regular expression, that plugin uses to search for word in each line of file

# Using

<img width="1310" height="340" alt="image" src="https://github.com/user-attachments/assets/621810db-919c-4210-8d10-823cc8a3f4b5" />

Trigger is ```dict ```, after entering that you will see list of all dictionaries you have, 
select the one you need and click tab, then enter the needed word. 

<img width="1312" height="654" alt="image" src="https://github.com/user-attachments/assets/ac699ad6-8e61-4348-919e-6dea08145c4f" />

You also can type ```\ ``` after dictionary is selected, that way you can disable basic regular expression 
and use your own (Python compatible) or don't use it at all
