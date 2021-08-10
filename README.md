# oswaveplus
This is just like the oswave player, but the first available (non-looped sound) is played with the winsound module

It has several advantages over the oswave player for Windows.
- Looped sounds are played with a command line instruction using the soundplayer always, there is essentially no delay between wave sounds.  This is an improvement.
- The first non-looped sound is played with the winsound module, so there is little delay.  Subsequent waves will play with a command line instruction unless the winsound module is not in use.

Put another way:
- All looped sounds loop with a loop instruction to powershell.
- All non-looped sounds use winsound module, unless in use then powershell.

So, this allows looped background sounds to be played essentially without delay between loops.  Sounds promptly play with winsound, but any additional sounds will not cancel winsounds play, but there is a little delay.

### This has no dependencies except what is typical in Linux (Alsa, standard part of Linux kernel), Afplay (standard on MacOS 10.5 and above), and the soundplayer module (Standard in Windows 10), and the Python Standard Library.

Works with wave files only.  Look at github/garydavenport73/oswaveplayer for a description of the functions, which are pretty much standard among my modules, so they can be dropped in place of each other.
