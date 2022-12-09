# bisync protocol
# Bradley Cox, 11/18/2022

# encode text data by converting text to hexadecimal and adding STX and ETX sentinels to beginning and end of string
def bisyncEncode(text):
    # convert text to hex
    encoded_text = text.encode('utf-8')
    hex_text = encoded_text.hex()

    # check to see whether or not the hex string contains the same characters as STX and ETX sentinels
    # if they already exist, character stuff with DLE (0x10)
    if "0x02" in hex_text:
        hex_text = hex_text.replace("0x02", "0x100x02")
    if "0x03" in hex_text:
        hex_text = hex_text.replace("0x03", "0x100x03")

    # add STX and ETX sentinels
    bisync_text = "0x02" + hex_text + "0x03"
    return bisync_text

# decode hexadecimal and convert back to plain text
def bisyncDecode(text):
    # check for sentinels at beginning and end
    if (text.index("0x02") == 0) and (text.index("0x03") == len(text) - 4):
        # check for DLE character stuffing, replace with temp value so they are not removed with sentinels
        if "0x100x02" in text:
            text = text.replace("0x100x02", "TEMP1")
        if "0x100x03" in text:
            text = text.replace("0x100x03", "TEMP2")

        # remove sentinels
        text = text.replace("0x02", "")
        text = text.replace("0x03", "")

        # replace temp values with original hex values
        if "TEMP1" in text:
            text = text.replace("TEMP1", "0x02")
        if "TEMP2" in text:
            text = text.replace("TEMP2", "0x03")

        # decode hexadecimal text to plain text
        decoded_text = bytes.fromhex(text).decode('utf-8')

        return decoded_text
    # if sentinels are not present, throw error
    else:
        print("invalid text")
        return

    

text = "hello world"

hex_text = bisyncEncode(text)

print(bisyncDecode(hex_text))


