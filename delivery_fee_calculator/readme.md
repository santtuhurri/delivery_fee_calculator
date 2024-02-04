Make sure that you have extracted all the files from the Zip archive, then selected "File ->" "Open Folder..." and folder called "delivery_fee_calculator". The folder tree should look like this:

-delivery_fee_calculator
    |           |-delivery_fee_calculator.py 
    |           |-delivery_fee_calculator_tests.py
    |           |-readme.md 
    |
    |-delivery_fee_calculator_api
            |       |-manage.py
            |
            |-calculator
            |-delivery_fee_calculator_api

Also make sure that you have installed and enabled "Python" extension from "Extensions" tab. If you don't have "Python", you can use the search bar in "Extensions" tab to find it, select it and choose "Install". Also make sure that it is Enabled.

This Zip archive contains "delivery_fee_calculator.py" that is the alpha version of this calculator. With this file it is possible to test how the calculator works on its own. All you need to do is Run the python file, or if you would like to, you can also change the values in row 73. Make sure to give cart_value, delivery_distance and number_of_items value as Integer and time value as String, otherwise you will receive "Error: Invalid input. Check your input values.".

"delivery_fee_calculator_tests.py" is used to test the functionality of "deliver_fee_calculator.py". It contains one(1) performance test and nine(9) unit tests for different occasions. These tests can be run by pressing "Run python file" button. Please don't change the values in this file.

Follow these steps in order to use calculator app that calculates delivery fee based on the cart value, the number of items in the cart, the time of the order and the delivery distance.

1. Run the command "pip install django" in the terminal (if you don't see the terminal, from the top banner select "View" -> "Terminal") to install Django that is needed to use the calculator.
2. If you receive "[notice] A new release of pip available: 22.3.1 -> 23.3.2", run the command "python.exe -m pip install --upgrade pip" to update it (If you run in to an error while installing, make sure that you are running your IDE as administrator). Now run the previous command "pip install django" again.
3. Once you have Django installed, you are ready to try the calculator.
4. Make sure that you are in the right folder. From your terminal you can see the current folder you are at and it should be something like this: C:\yourfolderpath\delivery_fee_calculator\delivery_fee_calculator_api. Most likely you are in C:\yourfolderpath\delivery_fee_calculator.
5. If you happen to be in the right folder, you can type "ls" to check that there is "manage.py" in that folder.
6. If you are NOT in the right folder, you need to locate where you extracted the Zip archive and move to that folder. You can use "cd .." and "cd 'foldername'" to move inside the folders. 

    - For bash and Command Promt use: "cd.." to move back and "cd deliver_fee_calculator_api" to move forward in the folders

    - For powershell use: "cd.." and "cd .\delivery_fee_calculator_api\"

    - You can also type "cd del" and press "TAB"and the terminal will automatically fill the command and you can search for the correct folder.

7. Run the command "python manage.py runserver" to start the development server. You should see the following text "Starting development server at http://127.0.0.1:8000/".
8. There are several ways to try out the calculator application, notice that you can't run commands on the same terminal where you started the server. You need to open a new terminal window. Feel free to change the values as you like, just make sure that cart_value, delivery_distnace and number_of_items values are Integers and time value is String.

    - For bash use: curl --location --request POST 'http://localhost:8000/' --header 'Content-Type: application/json' --data-raw '{ "cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}'

    - For Command Promt use: curl --location --request POST "http://localhost:8000/" --header "Content-Type: application/json" --data-raw "{\"cart_value\": 790, \"delivery_distance\": 2235, \"number_of_items\": 4, \"time\": \"2024-01-15T13:00:00Z\"}"

    - For powershell use: Invoke-RestMethod -Uri "http://localhost:8000/" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}'

9. You can also install "REST Client" extension to see a more detailed information. Once you have installed the extension, open a new file ("File" -> "New file...") and press "Enter". On the new file click "Select a language" or choose "View" -> "Command Palette..." and type "Change language mode", then select "HTTP (http)".
10. Copy the command for bash (section 8.) and paste it into the new file and press "CTRL" + "ALT" + "R" to send the request.
11. New window should open with information and response payload that contains the delivery fee in cents.
12. Now you have tested the calculator that counts the delivery fee based on the cart value, the number of items in the cart, the time of the order and the delivery distance.
13. You can press "CTRL" + "C" to shutdown the server.

Thank you for trying my calculator.

Creator of this application: Santtu Hurri - hurri.santtu@gmail.com