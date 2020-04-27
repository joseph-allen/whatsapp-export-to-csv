import io
import re
import sys
import argparse
import datetime
import xlwt
from datetime import date
from tqdm import tqdm


class dateFormats:
    # Define the time formats
    # English
    dateStrEN = "EN"
    dateEN = r"""^((\d{1,2})\/(\d{1,2})\/(\d{1,2}))"""
    dateFormatEN = "%d/%m/%y"
    timeFormatEN = "%I:%M:%S %p"
    patternEN = dateEN + \
        r"""\,\ \b((1[0-9]|0?[1-9])\:([0-5][0-9])\:([0-5][0-9])\ ([AaPp][Mm]))\:[^:](.+?)\:\ (.*)"""


class lastentry:
    lastlang = ""
    lastdate = date.today()
    lasttime = date.today()
    lastname = ""


def parse(line, verbose, debug):
    prefix = "***"
    dateLANG = dateFormats.dateEN
    dateFormatLANG = dateFormats.dateFormatEN
    timeFormatLANG = dateFormats.timeFormatEN
    pattern = dateFormats.patternEN
    pattern = "^((\d{1,2})([\/|\.])(\d{1,2})[\/|\.](\d{1,2}))\,\ (\d{1,2}:\d{1,2})(?::\d{1,2})?\ ?(AM|PM|am|pm)?([\:\ |\ \-\ ][^:])(.+?)\:\ (.*)"
    found = ""
    dataset = ['empty', '', '', '', '', '']

    if (re.match(re.compile(dateFormats.dateEN, re.VERBOSE), line)):
        # English
        dateStr = dateFormats.dateStrEN
        dateLANG = dateFormats.dateEN
        dateFormatLANG = dateFormats.dateFormatEN
        timeFormatLANG = dateFormats.timeFormatEN
        found = dateFormats.dateStrEN

    else:
        if debug:
            print("Appending line found")
        newline = (re.match(re.compile(r"^(.*)", re.VERBOSE), line))

        if (1):
            dataset = ['new', lastentry.lastdate, lastentry.lasttime,
                       lastentry.lastname, newline.group(0)]

        else:
            # Otherwise make sure it is appended to the existing line
            dataset = ['append', '', '', '', newline.group(0)]
            if (verbose | debug):
                print(dataset)

    if (len(found) > 0):
        # Make the match, assign to the groups
        match = re.match(re.compile(pattern, re.VERBOSE), line)

        if (match and match.group(9) != 'M'):
            # 21/12/19 Date Format
            if (match.group(3) == '/' and match.group(8) == ': '):
                date = datetime.datetime.strptime(
                    match.group(1), "%d/%m/%y").date()
            # 12/21/19 Date Format
            elif (match.group(3) == '/' and match.group(8) == ' -'):
                date = datetime.datetime.strptime(
                    match.group(1), "%m/%d/%y").date()
            # 21.12.19 Date Format
            else:
                date = datetime.datetime.strptime(
                    match.group(1), "%d.%m.%y").date()

            if (match.group(7)):
                time = datetime.datetime.strptime(match.group(
                    6) + " " + match.group(7), "%I:%M %p").time()
            else:
                time = datetime.datetime.strptime(
                    match.group(6), "%H:%M").time()

            # Buffer date, time, name for next line messages
            lastentry.lastlang = dateStr
            lastentry.lastdate = date.strftime("%Y-%m-%d")
            lastentry.lasttime = time.strftime("%H:%M")
            lastentry.lastname = match.group(9)

            # Create the dataset for the new message
            dataset = ['new', date.strftime(
                "%Y-%m-%d"), time.strftime("%H:%M"), str(match.group(9)), match.group(10)]
            if (verbose | debug):
                print(dataset)

    return dataset


def convert(filename, resultset='resultset.csv', verbose=False, debug=False):
    # Store the number of lines of the input file
    line_count = 0

    try:
        # Count the number of total lines
        with io.open(filename, "r", encoding="utf-8") as file:
            for line in file:
                # if line.strip():
                line_count += 1

        # Convert lines to csv
        with io.open(filename, "r", encoding="utf-8") as file:
            content = file.readlines()

    except IOError as e:
        print("File \"" + filename + "\" cannot be found.")
        sys.exit()

    print("Converting data now")

    # Count number of chatlines without empty lines
    counter = 0

    if (debug):
        print("Open export file " + resultset[0])

    # Define export file header
    header = ['datetime', 'name', 'message']

    # Select export formats
    if str(resultset[0]).endswith('.csv'):

        # Open result filename
        csv = io.open(resultset[0], "w", encoding="utf-8")

        # Write headers
        csv.write(header[0] + '|' + header[1] + '|' + header[2] + '\n')

    elif str(resultset[0]).endswith('.ods'):
        wb = xlwt.Workbook()
        ws = wb.add_sheet(filename)

        ws.write(0, 0, header[0])
        ws.write(0, 1, header[1])
        ws.write(0, 2, header[2])

        ws_counter = 1

    # Show progress via tqdm
    for line in tqdm(content, total=line_count, ncols=120):
        if (debug and line == ''):
            print(line)
        dataset = parse(line, verbose, debug)
        if (dataset[0] != 'empty'):

            # Write to .csv file
            csv.write(dataset[1] + ' ' + dataset[2] +
                      '|' + dataset[3] + '|' + dataset[4] + '\n')

        # Print progress
        if line.strip():
            counter += 1

    print('Wrote ' + str(counter) + ' lines')

    # Close the resultfiles
    if str(resultset[0]).endswith('.csv'):
        csv.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", help="the WhatsApp file containing the exported chat")
    parser.add_argument("resultset", help="filename of the resultset, default resultset.csv. Use .csv to write a comma separated file. Use .ods to write to a LibreOffice spreadsheet file", default="resultset.csv", nargs='*')

    args = parser.parse_args()

    convert(filename=args.filename, resultset=args.resultset)
