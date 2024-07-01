import os, datetime, shutil, pyfastcopy

import time



list_path = []
today = datetime.date.today()

def search_path():
    # Your list of folder names
    folder_names = input("""Introduce the shots in a line with spaces: """).split()
    # Loop through each folder name
    for folder_name in folder_names:
        # Construct the full path
        base_path = "/Users/cao/Desktop/proyectos"
        full_path = (f"""{base_path}/{folder_name[0:3]}/VFX/{folder_name[4:7]}/{folder_name[:-5]}/renders/4k/{folder_name}/""")
        print(folder_name)
        # Check if the folder exists
        # Add the paths to a list
        if os.path.isdir(full_path):
            print(f"\nFolder found: {full_path}\n")
            list_path.append(full_path)
        else:
            print(f"\nFolder not found: {full_path}\n")
    # Define the name of the project
    project = (str(folder_name[:3]))
    # Return the list of paths and project name  
    return list_path, project

def dest_folder(project):
    # Set destination folder
    source_folder = "/Users/cao/Desktop/proyectos/entregas"
    # Specify subfolder for project and date
    dest_path = (f"{source_folder}/{project}/{today.strftime('%Y%m%d')}_EXR")
    # Create folder if it doesn't exist
    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok=True)
    # Get the destination path for copy    
    return dest_path

def copy_folders():
    # Set the handles of the project
    handles = int(input("Set the handles of the project: "))
    # Set the extensions for the files to copy
    exclude_extensions = (".log", ".nk", ".temp")
    include_extensions = (".txt", ".exr", ".tiff", ".tif", ".dpx")
    # For loop for each shot
    for file in list_path:
        # Create the folder with the shot name
        folder_name = os.path.basename(file[:-1])
        final_path = os.path.join(dest_path, folder_name)
        # Check for subfolders
        sub_directories = [dir for root, dir, r in os.walk(file) if dir]
        if sub_directories:
            subfolders = sub_directories[0]
        else:
            subfolders = [] 
        # Omit the files you don't want
        frame_range = [f for f in os.listdir(file) if f.endswith(include_extensions)]
        frame_range.sort()
        excluded_handles = frame_range[:handles] + frame_range[-handles:]
        excluded_ext = [f for f in os.listdir(file) if f.endswith(exclude_extensions)]
        excluded_files = excluded_ext + excluded_handles + subfolders
        # Let's copy it!
        try:
            shutil.copytree(file[:-1], final_path, ignore=shutil.ignore_patterns(*excluded_files))
            print(f"{os.path.basename(file[:-1])}: SUCCEED!")
            # Check if there are any subfolders
            if not subfolders == []:
                # Arrange the paths
                for index, subfolder in enumerate(subfolders):
                    sfolder_path = file + subfolder
                    sfolder_dest = os.path.join(final_path, subfolder) 
                    # Omit the files you don't want
                    sframe_range = [f for f in os.listdir(sfolder_path) if f.endswith(include_extensions)]
                    sframe_range.sort()
                    sexcluded_ext = [f for f in os.listdir(sfolder_path) if f.endswith(exclude_extensions)]
                    sexcluded_handles = sframe_range[:handles] + sframe_range[-handles:]
                    sexcluded_files = sexcluded_ext + sexcluded_handles
                # Let's copy it!    
                    try:
                        shutil.copytree(sfolder_path, sfolder_dest, ignore=shutil.ignore_patterns(*sexcluded_files))
                        print(f"{subfolder}: SUCCEED!")
                    except Exception as e:
                        print(f"There has been an error with {subfolder}: {e}")  
            else:
                continue            
        except Exception as e:
            print(f"There has been an error: {e}")
                    



list_path, project = search_path()
dest_path = dest_folder(project)
start_time = time.time()
copy_folders()

print("--- %s seconds ---" % (time.time() - start_time))