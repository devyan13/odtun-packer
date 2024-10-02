import platform
import time
import tkinter as tk
import zipfile
import xml.dom.minidom
import os
import shutil
from tkinter import filedialog


def unpack_from_odt():
    # Step 1: Unzip the ODT file to a temporary directory
    odt_file = filedialog.askopenfilename(title="ODT-Datei auswählen", filetypes=[("ODT-Dateien", "*.odt")])
    temp_dir = 'temp_odt_content'

    with zipfile.ZipFile(odt_file, 'r') as z:
        z.extractall(temp_dir)

    # Step 2: Prettify the content.xml
    content_xml_path = os.path.join(temp_dir, 'content.xml')
    with open(content_xml_path, 'r', encoding='utf-8') as content_file:
        xml_content = content_file.read()

    # Step 3: Parse and prettify the XML content
    dom = xml.dom.minidom.parseString(xml_content)
    pretty_xml = dom.toprettyxml(indent="  ")

    # Step 4: Overwrite the content.xml with the prettified version
    with open(content_xml_path, 'w', encoding='utf-8') as content_file:
        content_file.write(pretty_xml)
    # when done, color the  button green
    time.sleep(2)

def pack_to_odt():
    temp_dir = 'temp_odt_content'
    new_odt_file = filedialog.asksaveasfilename(title="ODT-Datei speichern", filetypes=[("ODT-Dateien", "*.odt")])
    with zipfile.ZipFile(new_odt_file, 'w', zipfile.ZIP_DEFLATED) as z:
        for foldername, subfolders, filenames in os.walk(temp_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                # Keep the directory structure inside the zip file
                arcname = os.path.relpath(file_path, temp_dir)
                z.write(file_path, arcname)
    shutil.rmtree(temp_dir)
    # when done, color the  button green
    time.sleep(2)



def open_xml():
    system =platform.system()
    try:
        if system == "Windows":
            os.system("start " + "temp_odt_content/content.xml")
        elif system == "Linux":
            os.system("xdg-open " + "temp_odt_content/content.xml")
        elif system == "Darwin":
            os.system("open " + "temp_odt_content/content.xml")
    except Exception as e:
        print(e)



main = tk.Tk()
main.config(bg="#E4E2E2")
main.title("ODT un/packer")

odtunpack = tk.Button(master=main, text="ODT entpacken")
odtunpack.config(bg="#E4E2E2", fg="#000", command=unpack_from_odt)
odtunpack.pack(side=tk.LEFT, padx=10, pady=10, anchor='nw')


opencontent = tk.Button(master=main, text="Inhalt anzeigen")
opencontent.config(bg="#E4E2E2", fg="#000", command=open_xml)
opencontent.pack(side=tk.LEFT, padx=10, pady=10, anchor='nw')

odtpack = tk.Button(master=main, text="ODT packen")
odtpack.config(bg="#E4E2E2", fg="#000", command=pack_to_odt)
odtpack.pack(side=tk.LEFT, padx=10, pady=10, anchor='nw')


main.mainloop()


