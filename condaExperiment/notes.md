Need conda set up and installed

Conda user guide:
https://docs.conda.io/projects/conda/en/latest/user-guide/index.html

Anaconda download:
https://www.anaconda.com/products/individual

Getting started guide:
https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html

Add conda to path if you want to be able to use them from terminals other than "Anaconda Prompt" (see https://stackoverflow.com/questions/44597662/conda-command-is-not-recognized-on-windows-10).
Command to add to path:
```
set PATH=%PATH%;C:\Anaconda3;C:\Anaconda3\Scripts\
```
or search for "edit enironment variables for your account" in windows and add to `Path` there.

Before using `conda` in a different terminal, run `conda init` and then `conda init bash` (replace `bash` with the terminal you want) in the terminal you wish to use.

If you're using gitbash, you also need to run this command to get it to recognise conda (see https://superuser.com/questions/1479075/installing-anaconda-on-git-bash-and-trying-conda-activate-results-in-repeated-co and https://stackoverflow.com/questions/54501167/anaconda-and-git-bash-in-windows-conda-command-not-found):
```
echo '. ${HOME}/.bash_profile' >> ~/.bashrc
```