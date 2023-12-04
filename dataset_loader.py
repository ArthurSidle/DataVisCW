import numpy as np
import pandas as pd
from zipfile import ZipFile
import gzip
import concurrent
import zlib
import gc

class DatasetLoader:
    def __init__(self, file, csv, index_col=False, file_type='zip', lines=-1, max_blocks=-1):
        self.file = file
        self.csv = csv
        self.index_col = index_col
        self.file_type = file_type
        self.lines = lines
        self.max_blocks = max_blocks
        self.eof = False
        self.encoding = 'utf_8'
        self.prefix = 'data/'
        #self.lock = Lock()

    def set_file(self, file, csv):
        self.file = file
        self.csv = csv

    def decompress_data(self):
        block = 0

        if self.file_type == 'zip':
            with ZipFile(f'{self.prefix}{self.file}.zip') as archive:
                file = archive.open(f'{self.csv}.csv')
                df = pd.read_csv(file, index_col=self.index_col)
                file.close()
            return df
        elif self.file_type == 'gz':
            with gzip.open(f'{self.prefix}{self.file}.csv.gz') as archive:
                df = pd.read_csv(archive, index_col=self.index_col)
            return df
        else:
            return None

    def decompress_stream(self):
        if self.file_type == 'gz':
            self.archive = gzip.GzipFile(f'{self.prefix}{self.file}.csv.gz', mode='rb')

            line_str = self.archive.readline().decode(self.encoding).replace('\n', '')
            self.headers = np.array(line_str.split(','), dtype=np.str_)

            block = 0
            while self.eof == False:
                #print('Loading block ' + str(block))

                with concurrent.futures.ThreadPoolExecutor(1) as executor:
                    fragment = executor.submit(self.process_fragment).result()

                block += 1
                if block == self.max_blocks:
                    self.eof = True

                yield fragment

    def process_fragment(self):
        #df_data = np.empty(shape=(self.lines, self.headers.size), dtype='O')
        df_data = []
        for i in range(0, self.lines):
            try:
                line_str = self.archive.readline().decode(self.encoding).replace('\n', '')

                if line_str == '':
                    if i == 0:
                        self.eof = True
                else:
                    input_data = np.array(line_str.split(','), dtype=np.str_)

                    if input_data.size < self.headers.size:
                        input_data = np.pad(input_data, (self.headers.size - input_data.size, 0), 'constant', constant_values='0')

                    if input_data.size == self.headers.size:
                        df_data.append(input_data)

                    #if i % 100 == 0:
                    #    print(i)
                    #    print(df_data[0])

            except zlib.error:
                #print('zlib error')
                pass

        df = pd.DataFrame(df_data, columns=self.headers)
        return df