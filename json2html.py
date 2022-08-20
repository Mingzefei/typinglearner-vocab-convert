#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File : json2html.py
@Time : 2022/08/20 22:44:07
@Auth : Ming(<3057761608@qq.com>)
@Vers : 1.0
@Desc : json2html for Typing Learner
@Usag : python json2pdf.py -h|i|o|c
"""
# here put the import lib
import json
import pandas as pd
import sys

class Vocabulary:
    """
    :param path: path of json file
    """

    def __init__(self, path) -> None:
        # read json
        f = open(path, 'r')
        content = json.loads(f.read())
        f.close()
        
        self.name = content['name']
        self.type = content['type']
        self.language = content['language']
        self.size = content['size']
        self.relateVideoPath = content['relateVideoPath']
        self.subtitlesTrackId = content['subtitlesTrackId']
        self.wordList = content['wordList']

    def toHtml(self, outCols=['value','ukphone','translation']):
        """
        return html string

        """
        word = pd.DataFrame(self.wordList)
        # add [] for usphone and ukphone
        word['ukphone'] = word['ukphone'].map(lambda x: '['+x+']')
        word['usphone'] = word['usphone'].map(lambda x: '['+x+']')
        # replace '/n' for ;
        word['definition'] = word['definition'].map(lambda x: x.replace('\n', '; '))
        word['translation'] = word['translation'].map(lambda x: x.replace('\n', '; '))
        # if cannot find outCols, add new BLANK columns
        for col in outCols:
            if col not in [dfCol for dfCol in word]:
                word[col] = ''

        originHtml = word.to_html(columns=outCols, justify='center', col_space=50)
        modifyHtml = originHtml.replace('class', 'cellspacing=\"0\" class')
        return modifyHtml

def print_help():
    print('Desc : json2html for Typing Learner Vocabulary')
    print('Usag : python json2html.py -[h|i|o|c]')
    print('  -h : print help')
    print('  -i : Vocabulary path, like ./test/test1.json')
    print('  -o : output HTML path, like ./test/test1.html')
    print('  -c : HTML table columns, like value,ukphone,translation')

def main():
    if '-h' in sys.argv:
        print_help()
        sys.exit(0)

    inputPath = sys.argv[sys.argv.index('-i')+1]
    outputPath = sys.argv[sys.argv.index('-o')+1]
    if '-c' in sys.argv:
        columns = sys.argv[sys.argv.index('-c')+1]
    else:
        columns = ['value','ukphone','translation']
    
    my_vocabulary = Vocabulary(inputPath)
    outFile = open(outputPath, 'w')
    outFile.writelines(my_vocabulary.toHtml(outCols=columns))
    outFile.close()
    pass

if __name__ == '__main__':
    main()
