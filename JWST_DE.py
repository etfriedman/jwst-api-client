#!/usr/bin/env python3
import argparse, requests, json, os, urllib.request


DEAFULT_URL = "https://api.jwstapi.com/"
DEAFULT_API_KEY = "X"
DATA_INFO_FORMAT_MSG = "\nThe format of this output is as follows:\ndatasuffix: description\nInstruments used to create this type of data"

SPLASH_TEXT_ASCII = """Welcome to the....
       ___          _______ _______   ______            _                     
      | \ \        / / ____|__   __| |  ____|          | |                    
      | |\ \  /\  / / (___    | |    | |__  __  ___ __ | | ___  _ __ ___ _ __ 
  _   | | \ \/  \/ / \___ \   | |    |  __| \ \/ / '_ \| |/ _ \| '__/ _ \ '__|
 | |__| |  \  /\  /  ____) |  | |    | |____ >  <| |_) | | (_) | | |  __/ |   
  \____/    \/  \/  |_____/   |_|    |______/_/\_\ .__/|_|\___/|_|  \___|_|   
                                                 | |                          
                                                 |_|                          
"""

HELP_COMMANDS_MSG = """Setting parameters:
>> program "programID" - set the program id to search. "search" command will not return data if this has not been set.
>> dt "datatype" - Replace "datatype" with the type of data you would like searches to return. Enter "datainfo" for more information on what data is availble to be returned. Note the deafult data type to return is "thumb" for image thumbnails. 
>> ft "filetype" - set filetype for search
>> search - returns available data. Best used for specific searches when all three params are set (programID, datatype, filetype). Without programID this will return nothing.
>> program/dt/ft reset - reset specific parameter (ex: program reset -> program: none)


Information commands:
>> list - list available program ID's and their descriptions, to search
>> list programID - Returns a description of the program, the region/object JWST observed, any other useful information.
>> datainfo - list available types of data that can be searched
>> filetypes - lists available filetypes (or pick from these: jpg, ecsv, fits, json) 
"""
# Possible other commands
# >> ff filetype - return data from all programs with specific filetype, good for bulk search/download.
# >> fd datatype - return data from all prgrams with specific datatype
# >> filterD - filter current data by datatype suffix
# >> filterF - filter current data by filetype
# API Key not set:
# """


class Client:
    
    filetypes = ['jpg', 'ecsv', 'fits', 'json']
    programs = [2731, 2732, 2733, 2734]
    suffixes = ['ami', 'amiavg', 'aminorm', 'asn', 'c1d', 'cal', 'calints', 'cat', 'crf', 'crfints', 'dark', 'i2d', 'msa', 'phot', 'pool', 'psf-amiavg', 'psfalign', 'psfstack', 'psfsub', 'rate', 'rateints', 's2d', 's3d', 'thumb', 'trapsfilled', 'uncal', 'wfscmb', 'whtlt', 'x1d', 'x1dints']
    
    def __init__(self, args):
        if args.api_key == "X":
            gen_key = input("An API key must be generated to fetch data. Would you like to make one now? y/n\n\n> ").lower()
            if gen_key == "y":
                email = input("Enter your email, your API key will be sent there. Refer to README for how to use it with this program.\n\n> ")
                self.gen_api(email)
            else:
                print("The README has information on how to generate a key yourself.")
                exit(0)
        self.api_key = args.api_key    
        self.program_list_url = "https://api.jwstapi.com/program/list?"
        print(SPLASH_TEXT_ASCII)
        self.should_run = True
        self.url = "https://api.jwstapi.com/"
        self.data_info_set = False
        self.data_info = []
        
        self.programID = "None"
        self.datatype = "None"
        self.filetype = "None"
        self.current_data = []

        
        
    def run(self):
        print("For a list of commands, type 'help'")
        # Ask user what they want to do:
        # List Programs: https://www.stsci.edu/jwst/science-execution/approved-programs
        # Have a list of default programs that contain interesting sources
        # Fetch available programs:
        
        
        while self.should_run:
            print(f"\nProgram: {self.programID}\nDatatype: {self.datatype}\nFiletype: {self.filetype}")
            cmd = input("> ")
            
            if len(cmd.split()) < 2:
                if cmd == "help":
                    self.print_help()
                elif cmd == "datainfo":
                    self.get_data_info()
                elif cmd == "reset":
                    print("Resetting all parameters...")
                    self.programID = "None"
                    self.datatype = "None"
                    self.filetype = "None"
                    self.current_data = []
                elif cmd == "clear":
                    os.system("clear")
                    print(SPLASH_TEXT_ASCII)
                elif cmd == "exit" or cmd == "quit":
                    self.exit_program()
                elif cmd == "filetypes":
                    print("Available filetypes: jpg, ecsv, fits, json")
                elif cmd == "list":
                    print("Available program IDs: 2731, 2732, 2733, 2734")
                elif cmd == "search":
                    self.search_data()
                else:
                    print("Unknown command. Type 'help' for a list of commands.")
                    
            elif len(cmd.split()) == 2:
                cmd = cmd.split()
                if cmd[0] == "list":
                    self.program_desc(cmd[1])
                # elif cmd[0] == "ff":
                #     self.find_file(cmd[1])
                elif cmd[0] == "program":
                    if int(cmd[1]) in self.programs:
                        self.programID = int(cmd[1])
                    elif cmd[1] == "reset":
                        self.programID == "None"
                    else:
                        print("Invalid program ID. Available IDs: 2731, 2732, 2733, 2734")
                # elif cmd[0] == "search":
                #     if cmd[1] in self.filetypes:
                #         self.search_data("sf")
                #     elif cmd[1] in self.datatype:
                #         self.search_data("sd")
                elif cmd[0] == "dt":
                    if cmd[1] not in self.suffixes:
                        print("Unknow datatype/suffix. Type datainfo for available datatypes (suffixes)")
                    elif cmd[1] == "reset":
                        self.datatype == "None"
                    else:
                        self.datatype = cmd[1]
                
                elif cmd[0] == "ft":
                    if cmd[1] not in self.filetypes:
                        print("Unknown filetype. Available filetypes: jpg, ecsv, fits, json.")
                    elif cmd[1] == "reset":
                        self.filetype == "None"
                    else:
                        self.filetype = cmd[1]
                else:
                    print("Unknown command. Type 'help' for a list of commands.")
                
        
    
    # When sorting by jpg files, downloads an image to a specified path (open folder browsing for downloading?)
    def download_data(self, data_index, filename):
        folder_name = "JWST_data"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        
        if data_index > len(self.current_data):
            print("Error downloading data.")
        else:
            # Ask for path to download data to
            # then download there
            download_url = self.current_data[data_index][2]
            file = download_url.split("/")[-1]
            # open file browser to select where to store file
            
            # see if need to specify filetype after filename
            print(f"Downloading {file} to JWST_data folder...")
            urllib.request.urlretrieve(download_url, f"JWST_data/{file}")
            
    
    def filter_data(self, data):
        # program and datatype(suffix) set, no filetype, filter programID search by datatype
        if self.datatype != 'None' and self.filetype == 'None':
            # filter based on datatype
            new_data = []
            for item in data:
                if item["details"]["suffix"] == f"_{self.datatype}":
                    new_data.append(item)
            return new_data
        # filetype set, no datatype, filter programID search by filetype
        if self.datatype == 'None' and self.filetype != 'None':
            new_data = []
            for item in data:
                if item["file_type"] == self.filetype:
                    new_data.append(item)
            return new_data
        # if both are set
        if self.datatype != "None" and self.filetype != "None":
            # filter based on filetype THEN datatype
            new_data = []
            for item in data:
                if item["file_type"] == self.filetype and item["details"]["suffix"] == f"_{self.datatype}":
                    new_data.append(item)
            return new_data
        if self.datatype == "None" and self.filetype == "None":
            return data
    
    
    # s - check programID set, filter for datatype and/or filetype
    # sf - dont care about programID, search by filetype
    # sd - dont care about programID, search by datatype (suffix)
    def search_data(self):
        # if self.programID == 'None' and self.datatype == "None" and self.filetype == "None":
        if self.programID == 'None':
            print("programID must be set to run a search, it is highly reccomended to set other params before running a search as well.") 
        else:
            # will always be correct programID
            # return all data from progrmas, listing length of response before printing
            # Normal JUST programID search, many results
            # dont need to check if correct id since when setting does the checks, same for other searches!@#!@#!@#!@#
            # if self.programID != 'None' and self.programID in self.programs and search_type == "s":
            # check programID set?
            self.url = f"https://api.jwstapi.com/program/id/{self.programID}" # programID search url
            # see return type for data (list of dict, onebig dict, etc.)
            res = self.send_request()
            # print(type(res))
            
            # iterate through each and get info
            # store in here, list of tuples
            data = res["body"]
            
            # filter data if FT and/or DT are set
            data = self.filter_data(data)
            items = []
            
            for key in data:
                items.append(self.parse_data(key))
                
            if len(items) == 0:
                print("No data avaiable with given params. Type reset to clear all params or change one and try again.")
                return
            else:
                print(f"Number of items returned: {len(items)}")
                self.current_data = items
                print_result = input("Print returned data? Type y/n. Note: A large number of items will fill up the command line.\n\n>")
                if print_result == "y":
                    item_count = 1
                    for i in self.current_data:
                        print(item_count)
                        item_count += 1
                        print(f"ObservationID: {i[0]}\nProgramID: {i[1]}\nLocation: {i[2]}\n")
                
                download = input("Select files for downloading?: y/n\n>").lower()
                if download == "y":
                    self.work_with_data()
                else:
                    return
                
                
    def work_with_data(self):
        # runs after search, self.current_data hold list of tuples containing data
        print("Select data to download. Enter a single number to download a specific file (e.g. 3), or enter a list of numbers seperated by commas to download multiple files (e.g. 1,2,5,24)")
        cmd = input(">")
        # select one
        if len(cmd) < 2:
            print(f"Downloading file at index: {cmd}")
            print("Saving files to folder 'JWST_data'")
            self.download_data(int(cmd)-1, "JWST_data")
        elif len(cmd) > 1:
            cmd = cmd.strip(" ")
            cmd = cmd.split(',')
            print("Saving files to folder 'JWST_data'")
            for item in cmd:
                print(f"Downloading files: {item}")
                self.download_data(int(item)-1, "JWST_data")
        else:
            print("invalid download index.")
            self.work_with_data()
         
                
    
    def gen_api(self, email):
        url = "https://api.jwstapi.com/api/key"
        payload = {'email': email}
        r = requests.request("POST", url, data=payload)
        # check if 200 returned?
        print(f"API key generated! An email has been sent to: {email} with the key. Refer to README on how to use with this program.")
        print("Make sure to check your spam/all mail folder for the email.")
        exit(0)
        
    def program_desc(self, programID):
        if int(programID) not in self.programs:
            print("Invalid program ID. Available IDs: 2731, 2732, 2733, 2734")
        else:
            if programID == "2731":
                print("""ERO observation of part of NGC 3324, a star-forming region in the Carina complex. This ERO captures a sharp edge between a bubble formed by
young, hot stars, and a dense cloud, adjacent to the region seen in a Hubble Heritage image, but brighter in the MIR. The pointing is selected to
maximize contrast at optical and mid-infrared wavelengths, while taking advantage of the likely roll angle at the time of observation.""")
                print("More info from the JWST proposal: https://www.stsci.edu/jwst/phase2-public/2731.pdf")
            elif programID == "2732":
                print("""ERO observations of the Stephan's Quintet compact Hickson Group. This proposal contains a large NIRCam imaging field, a smaller MIRI imaging
field, and NIRSpec IFU+MIRI MRS spectroscopy the NGC7319 Seyfert II core. The group consists of at least 5-6 individual large galaxies at z=0.02597, some of which are actively
interacting. One, NGC7319, harbors a bright Seyfert 2 core.""")
                print("More info from the JWST proposal: https://www.stsci.edu/jwst/phase2-public/2732.pdf")
            elif programID == "2733":
                print("""ERO of the planetary nebula NGC 3132 (AKA the southern ring). This ERO is NIRCam and MIRI imaging only, no spectroscopy. NGC3132 is
characterized by strong ionized and H2 lines (Monreal-Ibero et al, 2021; Mata et al. 2016).""")
                print("More info from the JWST proposal: https://www.stsci.edu/jwst/phase2-public/2733.pdf")
            elif programID == "2734":
                print("""ERO observations of a transit of the HAT-P-18b exoplanet. This proposal contains NIRISS SOSS spectroscopy of a single transit. This is a 9-group per integration, 469-integration time-series exposure that aims to target transit of the exoplanet HAT-P-18b using NIRISS/SOSS.""")
                print("More info from the JWST proposal: https://www.stsci.edu/jwst/phase2-public/2734.pdf")
                
    
    # return tuple with observationID, program, location
    def parse_data(self, data):
        # observationID
        observationID = data["observation_id"]
        # program number
        program = data["program"]
        # url of data
        location = data["location"]
        
        return (observationID, program, location)
    
    
    
    def find_file(self, ft):
        if ft not in self.filetypes:
            print("Unknown filetype. Available filetypes: " + ', '.join(self.filetypes))
        else:
            self.url = f"https://api.jwstapi.com/all/type/{ft}"
            res = self.send_request()
            (observationID, program, location) = self.parse_data(res)
            
            
        
    
    # Send a request given settings, returns text from return
    def send_request(self):
        print("Attempting send. URL: " + self.url)
        if self.api_key == "X":
            print("You must set an API key before searching. Type help for info on getting an API key (request can be made through this program!)")
            # self.run()
        else:
            headers = {"X-API-KEY": self.api_key}
            if len(headers) == 0:
                print("Error settings headers")
            else:
                r = requests.request("GET", self.url, headers=headers)
                return json.loads(r.text)
    
    def print_help(self):
        print("\nWelcome to the JWST data explorer! Currently available commands:")
        print(HELP_COMMANDS_MSG)
    
    def exit_program(self):
        print("\n\n Thank you for using the JWST CLI Data Explorer. -Ethan\n")
        exit(0)
        
    # generate currently available data and the instruments of the JWST used to creat it
    def get_data_info(self):
        if self.data_info_set:
            print("Data types and instruments:\n")
            for i in self.data_info:
                print(i)
            print(DATA_INFO_FORMAT_MSG)
            return
        else:
            # update url for suffix search
            self.url = "https://api.jwstapi.com/suffix/list"
            request = self.send_request()
            res_status_code = request["statusCode"]
            # check request was OK
            if res_status_code == 200:
                body = request["body"]
                # create string of this later when printing
                suffix_instruments = []
                temp_suff = []
                
                for item in body:
                    # remove splice if not needed / requires more data manipulation later
                    suffix = item["suffix"][1:]
                    desc = item["description"]
                    instrument_list = []
                    instruments = item["instruments"]
                    
                    for inst in instruments:
                        instrument_list.append(inst['instrument'])
                    
                    suffix_instruments.append(f"{suffix}: {desc}\nInstruments: {', '.join(instrument_list)}\n")
                    temp_suff.append(f"{suffix}")
                print("Data types and instruments:\n")
                for i in suffix_instruments:
                    print(i)
                print(DATA_INFO_FORMAT_MSG)
                # print(str(temp_suff))
                self.data_info = suffix_instruments
                self.data_info_set = True
            
                
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="JWST_DE", description='CLI for exploring/downloading/viewing available JWST data.', epilog="Created by Ethan Friedman. 2022. https://github.com/etfriedman", usage="./JWST_DE.py -key YOUR_API_KEY.\nNOTE: If this is your first time running the program, please see the README for info on how to get an API key, and how to make this program executable.\nAlternatively, you can run this program using the command: 'python3 JWST_DE.py -key YOUR_API_KEY")
    parser.add_argument('--key', dest="api_key", type=str, default=DEAFULT_API_KEY, help="Your JWST api key. Request one here: https://jwstapi.com/ (Scroll to bottom of page and enter you email).")
    args = parser.parse_args()
    client = Client(args)
    client.run()