## script for dumping edaalat.org data

this script is just for educational purposes, and it is not intended to be used for any illegal activities.

# Usage
```bash
// installing dependencies, creating virtual environment, and creting data directory
chmod +x setup.sh
./setup.sh

// activating virtual environment
source venv/bin/activate

// 1- change the starting page and ending page in the dump.py file, main method
// 2- running the script
python3 dump.py
```
# Collected Data

after running the script you will find the collected data in the data directory.

- data/data.text: Contrains All Case Details in single file 
- data/attachments: Contains all attachments that related to the cases (attachment/letter/report_CaseNumber_AttachmentNumber.html/pdf)

> NOTE: if you want cleaner data its simple to write the data to a csv or database, you need just modified the code in the dump.py file.