# whatsapp-export-to-csv
Converts Exported whatsapp chats from .txt to CSV. This may only work with EN enconded times.

Code based on [whatsapp-converter](https://github.com/sandsturm/whatsapp-converter)

# Installation
Install the requirements using pip3 as follows:
```
pip3 install -r requirements.txt
```

# Running
fill the the blanks.
```
python3 converter.py <INPUT.TXT> <OUTPUT.CSV>
```


## Conversion from to
Each line of the dataset will be converted to a CSV.
```
2/20/19, 10:14 PM - Messages to this group are now secured with end-to-end encryption. Tap for more info.
2/20/19, 10:14 PM - You created group "Example chat"
2/21/19, 9:09 AM - Joe: Wow what an amazing chat!
2/21/19, 9:10 AM - Dom: I agree, it is amazing!
2/21/19, 9:12 AM - Joe: You're the best!
2/21/19, 9:12 AM - Dom: No, you are the best!
```

The output file looks like this.
```
datetime|name|message|
2019-02-21 09:09| Joe|Wow what an amazing chat!
2019-02-21 09:10| Dom|I agree, it is amazing!
2019-02-21 09:12| Joe|You're the best!
2019-02-21 09:12| Dom|No, you are the best!

```
