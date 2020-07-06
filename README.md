## Recover an entire directory (recursively) with ```ddrescue```
**Manual:**
```
usage: ddrescue_dir.py [-h] [-n] [-i] [-v] [-q] [--no-log] [--no-scrape]
                       [--no-trim] [--ddpath DDPATH] [--options OPTIONS]
                       src_dir dst_dir

ddrescue directory - by /robex/

positional arguments:
  src_dir            source directory
  dst_dir            destination directory (source folder created
                     automatically)

optional arguments:
  -h, --help         show this help message and exit
  -n                 dry-run: dont copy files, only show commands
  -i                 interactive: ask for confirmation for each file
  -v                 verbose ddrescue mode
  -q                 quiet: dont display ddrescue output
  --no-log           do not store log files (use if know what you are doing!)
  --no-scrape        skip the scraping phase
  --no-trim          skip the trimming phase
  --ddpath DDPATH    path to ddrescue binary (only needed if not in $PATH)
  --options OPTIONS  any other options to be passed to ddrescue (see example below)
```

**Examples:**

Rescue directory /mnt/data and save it to /home/user/data:
```./ddrescue_dir.py /mnt/data/ /home/user/```

Rescue same directory, but retry reading failed sectors 10 times:
```./ddrescue_dir.py /mnt/data/ /home/user/ --options="-r 10"```
