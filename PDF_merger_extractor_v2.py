import PySimpleGUI as sg
import os
from PyPDF2 import PdfFileMerger


def check_if_selected_file(key):
    if values[key] != '':
        path = values[key]
        return path
    # else:
    #     sg.Popup(f'You need to select {key}!')


pdfs = []
# color = 'Dark'
# sg.change_look_and_feel('Light')

merge_layout = [[sg.Text('Choose files you want to merge:', size=(50, 1))],
                [sg.Input(key='_FILES_'), sg.FilesBrowse(button_text='Choose pdf files', key='pdfs')],
                [sg.Text('or choose the folder that you want to merge:', size=(50, 1))],
                [sg.Input(key='FOLDER'), sg.FolderBrowse(button_text='Choose folder', key='dir')],
                [sg.Text('Write the name of a new file')],
                [sg.Input(size=(35, 10), key='name_merged')],
                [sg.Ok(key="merge")]
                ]
extract_layout = [[sg.Text('Choose the file from which you want to extract pages:', size=(50, 1))],
                  [sg.Input(key='_FILE_'), sg.FileBrowse(button_text='Choose pdf file', key='pdf_extract')],
                  [sg.Text('From:'), sg.Input(key='start', size=(10, 1)), sg.Text('To:'),
                   sg.Input(key='stop', size=(10, 1))],
                  [sg.Text('Write the name of a new file')],
                  [sg.Input(size=(35, 10), key='INPUT')],
                  [sg.Text("")],
                  [sg.Ok(key="extract")]]

layout = [
    [sg.TabGroup([[sg.Tab('Merge', merge_layout,title_color='black'), sg.Tab('Extract', extract_layout)]])]]

# Create the Window
window = sg.Window('PDF MERGER', layout, resizable=True)
# Event Loop to process "events"
while True:
    try:

        event, values = window.Read()
        print(event, values)
        if event == 'merge':
            # MERGE
            merger = PdfFileMerger(strict=False)
            pdf_path = check_if_selected_file('pdfs')
            folder_path = check_if_selected_file('dir')
            if pdf_path is None and folder_path is None:
                sg.Popup(f'Please select a file or a folder')
                continue

            if folder_path is None:
                pdfs = values['_FILES_'].split(';')

            else:
                selected_folder = values['FOLDER']
                print(os.listdir(selected_folder))
                files = os.listdir(selected_folder)

                for file in files:
                    if file.endswith(".pdf"):
                        pdfs.append(file)

            for pdf in pdfs:
                merger.append(pdf)

            name_merged = values['name_merged']
            print(name_merged)
            if name_merged == "":
                sg.Popup('Please insert a name of a new file')
                continue
            merger.write(f"{name_merged}.pdf")
            merger.close()
            sg.Popup('All done')
        elif event == "extract":
            pdf_to_extract_path = check_if_selected_file('pdf_extract')
            if pdf_to_extract_path is None:
                sg.Popup('Please select a pdf file')
                continue
            pdf = values['_FILE_'].split(';')
            merger = PdfFileMerger(strict=False)

            start = int(values['start']) - 1
            stop = int(values['stop'])

            for page in pdf:
                # merger.append(page)
                merger.append(page, pages=(start, stop))  # first 3 pages
            # merger.append(pdf, pages=(0, 6, 2))  # pages 1,3, 5

            # NAME A NEW FILE
            name = values['INPUT']
            print(name)
            if name == "":
                sg.Popup('Please insert a name of a new file')
                continue
            #
            merger.write(f"{name}.pdf")
            merger.close()
            sg.Popup('All done')
            if event == 'Cancel':
                window.Close()
            else:
                break
        else:
            break
    except TypeError:
        break
    except Exception as e:
        sg.Popup(f'Something went wrong\n {e}')

window.Close()