### 1. There are three main ways to get help: man, --help, and help. Why do you think Linux has these different options instead of just one? In what specific scenario would help be the only correct choice?

- **man** - an interface to the system reference manuals. This is the traditional, in-depth reference and is available for most external commands and programs installed on your system

- **--help** option: When you add --help after a command (like ls --help), it quickly displays a summary of the command's options and usage directly in the terminal.

- **help** This is unique to shell built-ins (commands built into the shell, like Bash). Typing help [command] gives a brief explanation of built-in commands such as cd, export, or echo. It does not work with external commands;

When you want information about a shell built-in command (like cd, break, export, read, etc.), only the help command will work. Neither man nor --help typically provide documentation for built-ins, unless you consult the general Bash or shell manual.

---

### 2. What is the key difference between using ls | grep ".txt" and find . -name "\*.txt"? When would one be more powerful than the other?

ls | grep ".txt" lists .txt files only in the current directory and is simple but limited.

find . -name "\*.txt" searches recursively through all subdirectories, handles special characters well, and offers powerful filtering and actions.

ls will be powerfull if you know the sub directory and want fast results
find will be powerfull if you dont know the sub directory and want recursive search results

---

### 3. The document shows how ps aux | grep chrome can filter running processes. How could you use this same piping concept with the history command to find a specific command you ran last week?

Use history | grep "keyword" to quickly find past commands matching your keyword, just like filtering processes with ps aux | grep chrome.

```
 $ history | grep "ls"
```

---

### 4. Why might you choose to send a .tar.gz archive instead of a .zip file if you know the other developer is also using Linux? What security risk should you be aware of before extracting an archive you received from an unknown source?

Use .tar.gz on Linux to preserve permissions and get better compression.