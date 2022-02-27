#!/usr/bin/env python3

"""
goatparser v1.00 [10.07.2021] *** by fieserWolF
usage: goatparser.py [-h] [-o OUTPUT_FILE] input_file

This program parses C64 Goattracker source files.

positional arguments:
  input_file            goattracker .sng input file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        text output filename

Example: ./goatparser.py song.sng
"""

import os
import sys
import struct
import argparse



PROGNAME = 'goatparser';
VERSION = '1.00';
LAST_CHANGED = '27.02.2022';

buffer = []
offset = 0


REST_VALUE = 0x55
OFFNOTE_VALUE = 0x54


def _value_to_note(
    note
) :

    """
    Values $60-$BC are the notes C-0 - G#7
    Value $BD is rest
    Value $BE is keyoff
    Value $BF is keyon
    Value $FF is pattern end
    """
    
    REST_VALUE    = 0xbd
    KEYOFF_VALUE  = 0xbe
    KEYON_VALUE   = 0xbf
    PATTERN_END_VALUE = 0xff
        
    Name = (
        'C-0', 'C#0', 'D-0', 'D#0', 'E-0', 'F-0', 'F#0', 'G-0', 'G#0', 'A-0', 'A#0', 'B-0',
        'C-1', 'C#1', 'D-1', 'D#1', 'E-1', 'F-1', 'F#1', 'G-1', 'G#1', 'A-1', 'A#1', 'B-1',
        'C-2', 'C#2', 'D-2', 'D#2', 'E-2', 'F-2', 'F#2', 'G-2', 'G#2', 'A-2', 'A#2', 'B-2',
        'C-3', 'C#3', 'D-3', 'D#3', 'E-3', 'F-3', 'F#3', 'G-3', 'G#3', 'A-3', 'A#3', 'B-3',
        'C-4', 'C#4', 'D-4', 'D#4', 'E-4', 'F-4', 'F#4', 'G-4', 'G#4', 'A-4', 'A#4', 'B-4',
        'C-5', 'C#5', 'D-5', 'D#5', 'E-5', 'F-5', 'F#5', 'G-5', 'G#5', 'A-5', 'A#5', 'B-5',
        'C-6', 'C#6', 'D-6', 'D#6', 'E-6', 'F-6', 'F#6', 'G-6', 'G#6', 'A-6', 'A#6', 'B-6',
        'C-7', 'C#7', 'D-7', 'D#7', 'E-7', 'F-7', 'F#7', 'G-7', 'G#7', 'A-7', 'A#7', 'B-7' 
    )

    NORMAL_RETURN = 'NORMAL'
    REST_RETURN = '...'
    KEYON_RETURN = '###'
    KEYOFF_RETURN = '---'
    PATTERN_END_RETURN = 'END'
        
    if (note == REST_VALUE) : return REST_RETURN
    if (note == KEYON_VALUE) : return KEYON_RETURN
    if (note == KEYOFF_VALUE) : return KEYOFF_RETURN
    if (note == PATTERN_END_VALUE) : return PATTERN_END_RETURN

    note = note - 0x60
    return Name[note]
    



def _read_file(
    filename_in
) :
	#open input file
    print ("    Opening file \"%s\" for reading..." % filename_in)
    try:
        file_in = open(filename_in , "rb")
    except IOError as err:
        print("I/O error: {0}".format(err))
        sys.exit(1)

    # read file into buffer
    buffer=[]
    count = 0
    while True :
        data = file_in.read(1)  #read 1 byte
        if not data: break
        temp = struct.unpack('B',data)
        buffer.append(temp[0])
        count += 1

    file_in.close()

    return buffer




def _int_to_string(
    my_list
) :
    my_string = ''
    for i in my_list :
        if i != 0:
            my_string += chr(i)
    return my_string


def _read_string(
    size
) :
    global offset
    my_return = _int_to_string(buffer[offset:offset+size])
    offset += size
    return my_return

def _read_byte() :
    global offset
    my_return = buffer[offset]
    offset += 1
    return my_return



def _do_it(
    args
) :
    global buffer
        
    buffer = _read_file( args.input_file )


    #header
    """
    Offset  Size    Description
    +0      4       Identification string GTS5
    +4      32      Song name, padded with zeros
    +36     32      Author name, padded with zeros
    +68     32      Copyright string, padded with zeros
    +100    byte    Number of subtunes
    """
    header_id = _read_string(4)
    header_songname = _read_string(32)
    header_author = _read_string(32)
    header_copyright = _read_string(32)
    header_subtunes = _read_byte()

    """
    6.1.2 Song orderlists
    ---------------------

    The orderlist structure repeats first for channels 1,2,3 of first subtune,
    then for channels 1,2,3 of second subtune etc., until all subtunes
    have been gone thru.

    Offset  Size    Description
    +0      byte    Length of this channel's orderlist n, not counting restart pos.
    +1      n+1     The orderlist data:
                    Values $00-$CF are pattern numbers
                    Values $D0-$DF are repeat commands
                    Values $E0-$FE are transpose commands
                    Value $FF is the RST endmark, followed by a byte that indicates
                    the restart position
    """
    orderlist = []
    for j in range (0, header_subtunes) :

        subtune = []        
        for k in range (0, 3) :
            channel = []
            this_length = _read_byte()
            channel.append( this_length )

            this_entry = []            
            for i in range (0, this_length+1) :
                this_entry.append(_read_byte())

            channel.append(this_entry)      
            subtune.append(channel)

        orderlist.append(subtune)



    """
    6.1.3 Instruments
    -----------------

    Offset  Size    Description
    +0      byte    Amount of instruments n

    Then, this structure repeats n times for each instrument. Instrument 0 (the
    empty instrument) is not stored.

    Offset  Size    Description
    +0      byte    Attack/Decay
    +1      byte    Sustain/Release
    +2      byte    Wavepointer
    +3      byte    Pulsepointer
    +4      byte    Filterpointer
    +5      byte    Vibrato param. (speedtable pointer)
    +6      byte    Vibraro delay
    +7      byte    Gateoff timer
    +8      byte    Hard restart/1st frame waveform
    +9      16      Instrument name
    """
    instrument_amount = _read_byte()
    instrument_entry = []
    for i in range (0, instrument_amount) :
        entry = []
        entry.append(_read_byte())  #ad
        entry.append(_read_byte())  #sr
        entry.append(_read_byte())  #wave
        entry.append(_read_byte())  #pulse
        entry.append(_read_byte())  #filter
        entry.append(_read_byte())  #vibrato param
        entry.append(_read_byte())  #vibrato delay
        entry.append(_read_byte())  #gateoff timer
        entry.append(_read_byte())  #hardrestart/1st frame waveform
        entry.append(_read_string(16))  #instrument name
        instrument_entry.append(entry)
    

    """
    6.1.4 Tables
    ------------

    This structure repeats for each of the 4 tables (wavetable, pulsetable,
    filtertable, speedtable).

    Offset  Size    Description
    +0      byte    Amount n of rows in the table
    +1      n       Left side of the table
    +1+n    n       Right side of the table
    """
    wavetable_length = _read_byte()
    wavetable_entry_l = []
    for i in range (0, wavetable_length) :
        wavetable_entry_l.append(_read_byte())
    wavetable_entry_r = []
    for i in range (0, wavetable_length) :
        wavetable_entry_r.append(_read_byte())

    pulsetable_length = _read_byte()
    pulsetable_entry_l = []
    for i in range (0, pulsetable_length) :
        pulsetable_entry_l.append(_read_byte())
    pulsetable_entry_r = []
    for i in range (0, pulsetable_length) :
        pulsetable_entry_r.append(_read_byte())

    filtertable_length = _read_byte()
    filtertable_entry_l = []
    for i in range (0, filtertable_length) :
        filtertable_entry_l.append(_read_byte())
    filtertable_entry_r = []
    for i in range (0, filtertable_length) :
        filtertable_entry_r.append(_read_byte())

    speedtable_length = _read_byte()
    speedtable_entry_l = []
    for i in range (0, speedtable_length) :
        speedtable_entry_l.append(_read_byte())
    speedtable_entry_r = []
    for i in range (0, speedtable_length) :
        speedtable_entry_r.append(_read_byte())




    """
    6.1.5 Patterns header
    ---------------------

    Offset  Size    Description
    +0      byte    Number of patterns n

    6.1.6 Patterns
    --------------

    Repeat n times, starting from pattern number 0.

    Offset  Size    Description
    +0      byte    Length of pattern in rows m
    +1      m*4     Groups of 4 bytes for each row of the pattern:
                    1st byte: Notenumber
                              Values $60-$BC are the notes C-0 - G#7
                              Value $BD is rest
                              Value $BE is keyoff
                              Value $BF is keyon
                              Value $FF is pattern end
                    2nd byte: Instrument number ($00-$3F)
                    3rd byte: Command ($00-$0F)
                    4th byte: Command databyte
    """
    pattern_amount = _read_byte()
    pattern_length = []
    pattern_data = []
    for i in range (0, pattern_amount) :
        this_length = _read_byte()
        pattern_length.append(this_length)
        pattern_row = []
        for j in range (0, this_length) :
            this_row = []
            this_row.append(_read_byte()) #note
            this_row.append(_read_byte()) #instrument
            this_row.append(_read_byte()) #command1
            this_row.append(_read_byte()) #command2
            pattern_row.append(this_row)
        pattern_data.append(pattern_row)





    # do output
    output = []
    output.append("%s v%s [%s] *** by fieserWolF\n"% (PROGNAME, VERSION, LAST_CHANGED))
    output.append('-------------------\n')
    output.append('\n')

    output.append(str('id: "%s"\n' % header_id))
    output.append(str('name: "%s"\n' % header_songname))
    output.append(str('author: "%s"\n' % header_author))
    output.append(str('copyright: "%s"\n' % header_copyright))
    output.append('-------------------\n')
    output.append('\n')

    output.append(str('subtunes: $%02x\n' %header_subtunes))
    
    for i in range(0,header_subtunes) :
        output.append('\n')
        output.append(str('subtune: $%02x\n'%(i+1)))

        for j in range(0,3) :
            output.append('channel: %d / ' % (j+1))
            output.append('length: $%02x: ' % orderlist[i][j][0])
            for k in orderlist[i][j][1] :
                output.append(str('$%02x '%k))
            output.append('\n')
    output.append('-------------------\n')
    output.append('\n')


    output.append(str('instruments: $%02x\n' %instrument_amount))
    output.append('\n')
    
    for i in range(0,instrument_amount) :
        output.append('')
        output.append(str('$%02x '%(i+1)))
        output.append('"'+instrument_entry[i][9]+'"\n')
        output.append(str('adsr: $%02x%02x, ' %(instrument_entry[i][0],instrument_entry[i][1])))
        output.append(str('wave: $%02x ,'%(instrument_entry[i][2])))
        output.append(str('pulse: $%02x, '%(instrument_entry[i][3])))
        output.append(str('filter: $%02x ,'%(instrument_entry[i][4])))
        output.append(str('vibrato parameter: $%02x, '%(instrument_entry[i][5])))
        output.append(str('vibrato delay: $%02x, '%(instrument_entry[i][6])))
        output.append(str('gateoff timer: $%02x, '%(instrument_entry[i][7])))
        output.append(str('hardrestart/1rst frame waveform: $%02x, '%(instrument_entry[i][8])))
        output.append('\n')
        output.append('\n')
    output.append('-------------------\n')

    
    output.append('\n')
    output.append('wavetable (length: $%02x)\n'%wavetable_length)
    for i in range(0,wavetable_length) :
        output.append('%02x:%02x %02x\n'%(i,wavetable_entry_l[i], wavetable_entry_r[i]))
    output.append('-------------------\n')

    output.append('\n')
    output.append('pulsetable (length: $%02x)\n'%pulsetable_length)
    for i in range(0,pulsetable_length) :
        output.append('%02x:%02x %02x\n'%(i,pulsetable_entry_l[i], pulsetable_entry_r[i]))
    output.append('-------------------\n')

    output.append('\n')
    output.append('filtertable (length: $%02x)\n'%filtertable_length)
    for i in range(0,filtertable_length) :
        output.append('%02x:%02x %02x\n'%(i,filtertable_entry_l[i], filtertable_entry_r[i]))
    output.append('-------------------\n')

    output.append('\n')
    output.append('speedtable (length: $%02x)\n'%speedtable_length)
    for i in range(0,speedtable_length) :
        output.append('%02x:%02x %02x\n'%(i,speedtable_entry_l[i], speedtable_entry_r[i]))
    output.append('-------------------\n')



    output.append('\n')
    output.append('pattern (amount: $%02x)\n'%pattern_amount)

    output.append('\n')
    for no in range(0,pattern_amount) :
        output.append('pattern $%02x: length: $%02x\n'%(no,(pattern_length[i]-1)))
        for row in range(0,pattern_length[no]) :
            output.append('%02x: %s %02x %02x%02x\n'%(row,_value_to_note(pattern_data[no][row][0]), pattern_data[no][row][1], pattern_data[no][row][2], pattern_data[no][row][3]))
            #output.append('%02x: %02x %02x %1x%02x\n'%(row,pattern_data[no][row][0], pattern_data[no][row][1], pattern_data[no][row][2], pattern_data[no][row][3]))
        output.append('\n')
    output.append('-------------------\n')
        
        


    #save
    if (args.output_file) :
        filename_output = args.output_file
    else :
        filename_output = os.path.splitext(args.input_file)[0]+'.txt'

	#open output file
    print ("    Opening file \"%s\" for writing..." % filename_output)
    try:
        file_out = open(filename_output , "w")
    except IOError as err:
        print("I/O error: {0}".format(err))
        return None

    for i in output :
        file_out.write('%s' %i)

    file_out.close()

    
    print ("done.")
    
    return None




def _main_procedure() :
    print("%s v%s [%s] *** by fieserWolF"% (PROGNAME, VERSION, LAST_CHANGED))

    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='This program parses C64 Goattracker source files.',
        epilog='Example: ./goatparser.py song.sng'
    )
    parser.add_argument('input_file', help='goattracker .sng input file')
    parser.add_argument('-o', '--output', dest='output_file', help='text output filename')
    args = parser.parse_args()

    _do_it(args)


if __name__ == '__main__':
    _main_procedure()
