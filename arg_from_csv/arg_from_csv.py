'''
Created on 22 nov. 2016

@author: ferresdf
'''

import argparse
import sys
import csv
import getpass

class ArgFromCSV:
    "Base class that accept arguments from CSV File"
    
    def __init__(self, description, args):
        self.__needed_args = []
        # create argument parser
        self._arg_parser = argparse.ArgumentParser(description=description)
        # Add script arguments
        self._define_args()
        # Parse command line arguments
        self.__arguments = self._parse_argv(args)

        
        
        
    def __remove_none_args(self, dict):
        return {k:v for k,v in dict.items() if v is not None}
        
    def _define_args(self):
        self._arg_parser.add_argument('--csvfile', help='A csv file holding arguments')
    
    def _parse_argv(self, args):
        known, unknown = self._arg_parser.parse_known_args(args)
        return self.__remove_none_args(vars(known))
        
    def _add_needed_arg(self, *arg):
        for v in arg:
            self.__needed_args.append(v)
          
    def __ask_needed_missing_args(self, args):
    
        tmp_args = {}
        for v in self.__needed_args:
            if(not v in args):
                if(v == 'password'):
                    tmp_args[v] = getpass.getpass('Enter a value for {} : '.format(v))
                else:
                    tmp_args[v] = input('Enter a value for {} : '.format(v))
            
        # Check 
        tmp_args = self._check_args(tmp_args)
        
        args.update(tmp_args)
        self.__arguments.update(tmp_args)
        
        return args
    
    def __convert_to_argv(self, dict):
        result = []
        for k,v in dict.items():
            result.append('--{}'.format(k))
            result.append(v)
        return result
    
    def _script_content(self, args):
        pass
    
    def _check_args(self, args):
        return self._parse_argv(self.__convert_to_argv(args))
        
    def process(self):
        with open(self.__arguments['csvfile']) as csv_file:
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                # Check csv values with argument parser
                row = self._check_args(row)
                
                # Merge command line args with csv arguments. Command line args superseed csv args
                row.update(self.__arguments)
                
                # chek for missing args if this is the first data line
                if(reader.line_num == 2):
                    row = self.__ask_needed_missing_args(row)
                
                # Execute script
                self._script_content(row)
    
class DeactivateAP(ArgFromCSV):
    "Class That desactivate an wifi AP"

    def _define_args(self):
        super()._define_args()
        self._arg_parser.add_argument('--IP', type=int, help='AP IP address')
        self._arg_parser.add_argument('--header1', help='header1')
        self._arg_parser.add_argument('--header2', help='header2')
        self._arg_parser.add_argument('--header3', help='header3')
        self._arg_parser.add_argument('--header4', help='header4')
        self._arg_parser.add_argument('--header12', help='header12')
        
        self._add_needed_arg('IP', 'header12')
    
    def _test(self):
        pass
        
    def _script_content(self, args):
        print(args)
        #print(args['header1'])
        #print(args['header2'])
        #print(args['IP'])