import os, time, json


def calc_time(seconds):
    time_taken = []
    minutes = 0

    while seconds >= 60:
        minutes += 1
        seconds -= 60

    minutes = str(minutes)
    seconds = str(seconds)

    if len(seconds) == 1:
        seconds = "0" + seconds

    time_taken.append(minutes)
    time_taken.append(seconds)

    return time_taken


def make_directorys(DESTINATION_PATH):
    if not os.path.exists(DESTINATION_PATH):
        os.makedirs(DESTINATION_PATH)


def get_files_to_convert_input(SOURCE_PATH, PATH_CONVERTED, FOLDER_CONVERTED):
    files_to_convert_input = []
    if os.path.isdir(SOURCE_PATH):
        # [0]=paths, [1]=directorys, [2]=filenames
        for path, directorys, filenames in os.walk(SOURCE_PATH):
            if FOLDER_CONVERTED in directorys:
                directorys.remove(FOLDER_CONVERTED)
            for directory in directorys:
                destination_directory = path.replace(SOURCE_PATH, PATH_CONVERTED)
                make_directorys(os.path.join(destination_directory, directory))
            for file in filenames:
                if ".mp4" in file or ".vid" in file:
                    if ".xml" not in file:
                        source_file = os.path.join(path, file)
                        files_to_convert_input.append(source_file)
    return files_to_convert_input


def get_files_to_convert_output(FILES, PATH, DESTINATION_PATH):
    files_to_convert_output = []
    for file in FILES:
        destination_file = file.replace(PATH, DESTINATION_PATH)
        files_to_convert_output.append(destination_file)
    return files_to_convert_output


def main():
    time_start = time.time()

    FILE = "handbrake-settings.json"
    PATH = os.path.realpath(os.path.dirname(__file__))
    FOLDER_CONVERTED = "converted"
    os.chdir(PATH)

    with open(FILE, "r") as file:
        DATA = json.load(file)

    encoder =     DATA["encoder"]
    bitrate =     DATA["bitrate"]
    extra_flags = DATA["extra-flags"]

    if not os.path.exists(FOLDER_CONVERTED):
        os.makedirs(FOLDER_CONVERTED)

    PATH_CONVERTED = os.path.realpath(FOLDER_CONVERTED)

    files_input = get_files_to_convert_input(PATH, PATH_CONVERTED, FOLDER_CONVERTED)
    files_output = get_files_to_convert_output(files_input, PATH, PATH_CONVERTED)
    files_converted = os.listdir(FOLDER_CONVERTED)
    num_files = len(files_input)
    num_converted = 1
    finished = False

    try:
        for file in range(num_files):
            file_input = files_input[file]
            file_output = files_output[file]
            if file_input not in files_converted:

                if ".vid" in file_input:
                    file_output = file_output.replace(".vid", ".mp4")
                
                input_file = '"' + file_input + '"'
                output_file = '"' + file_output + '"'

                handbrake_str =  "HandBrakeCLI" + " -i " + input_file + " -o " + output_file + " -e " + encoder + " -b " + bitrate + extra_flags            
                # -i = Name of the input file
                # -o = Name of the output file
                # -e = Encoder ("x264", "nvenc_h264")
                # -b = Bitrate in kbit/s
                # -2 = Two Pass 
                # -T = Turbo (First run is faster)

                print("\n\n\n\n\nConverting ({num}/{total})\n".format(num = num_converted, total = num_files))

                os.system(handbrake_str)
                
                num_converted += 1

    except KeyboardInterrupt:
        finished = False
        print("\nKeyboard-Interrupt detected!")

    if finished:
        time_total = int(time.time() - time_start)
        time_total = calc_time(time_total)

        if num_converted > 1:
            print("\nFinished converting " + str(num_converted) + " files in " + str(time_total[0]) + ":" + str(time_total[1]) + " min")
        else:
            print("\nFinished converting " + str(num_converted) + " file in " + str(time_total[0]) + ":" + str(time_total[1]) + " min")  

    input("Press enter to exit: ")


if __name__ == "__main__":
    main()