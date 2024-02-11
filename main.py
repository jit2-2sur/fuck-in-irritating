"""main module"""

import uvicorn
from myapi import app

def main():
    '''Main function'''
    while True:
        print(f'''
        ---------- Welcome to my Q&A application -------------
              1. Upload pdf
              2. Ask Question and get answer
              3. Exit
        ''')
        try:
            user_choice = int(input('Enter your choice (in number/integer): '))
            if user_choice == 1:
                file_path= input('Enter file path: ')
                pdf_name= input('Enter pdf name: ')
                print('file uploaded successfully: ')
            elif user_choice == 2:
                question= input('Enter question: ')
                pdf_name= input('Enter pdf name: ')
                print('here is the answer: ')
            elif user_choice == 3:
                print('Exited from application successfully.')
                break
            else:
                print('Enter a valid choice')
        except ValueError:
            print('Please enter a valid choice')

if __name__ == "__main__":
    uvicorn.run("myapi:app", host="127.0.0.1", port=8000, reload=True)
    #main()