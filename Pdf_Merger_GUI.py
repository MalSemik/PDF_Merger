import PySimpleGUI as sg
from PyPDF2 import PdfFileMerger


def check_if_selected_file(key):
    if values[key] != '':
        path = values[key]
        return path
    else:
        sg.Popup(f'You need to select {key} file!')


pdfs = []
color = 'Dark'
sg.change_look_and_feel(color)

layout = [
    [sg.Text('Choose files you want to merge:', size=(50, 1))],
    [sg.Input(key='_FILES_'), sg.FilesBrowse(button_text='Choose pdf files', key='pdf')],
    [sg.Text('Write the name of a new file')],
    [sg.Input(size=(35, 10), key='INPUT')],
    [sg.OK(), sg.Cancel()]]

# Create the Window
window = sg.Window('PDF MERGER', layout, resizable=True)
# Event Loop to process "events"
while True:
    try:

        event, values = window.Read()
        print(event, values)
        if event == 'OK':
            pdf_path = check_if_selected_file('pdf')
            if pdf_path == None:
                continue
            pdfs = values['_FILES_'].split(';')
            merger = PdfFileMerger(strict=False)

            for pdf in pdfs:
                merger.append(pdf)
                # merger.append(pdf, pages=(0, 3))  # first 3 pages
                # merger.append(pdf, pages=(0, 6, 2))  # pages 1,3, 5
            name = values['INPUT']
            print(name)
            if name == "":
                sg.Popup('Please insert a name of a new file')
                continue
            merger.write(f"{name}.pdf")
            merger.close()
            sg.Popup('All done')
        if event in (None, 'Cancel'):
            break

    except Exception as e:
        sg.Popup(f'Something went wrong\n {e}')



window.Close()
