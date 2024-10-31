import requests, threading, base64

account = {}
latest_balance = 0

def login(email, password):
    data = {
        'email_address': email,
        'password': password
    }
    response = requests.post('https://earnlink.app/sign-in/process-request/', data=data)
    data = response.json()
    account.update(response.cookies.get_dict())
    return data

def answer(ans):
    global latest_balance
    data = {
        'code_enter': ans
    }
    response = requests.post('https://earnlink.app/math-solve/process-data.php', data=data, cookies=account)
    data = response.json()
    latest_balance = data['available_balance']
    return

def get_question():
    response = requests.get('https://earnlink.app/math-solve/server.php', cookies=account)
    data = response.json()
    return data

def tryagain():
    print("Do you want to try again? (Y/N)")
    choice = input("Enter choice: ")
    if choice.lower() == 'n':
        return False
    elif choice.lower() == 'y':
        return True
    else:
        print("Invalid choice")
        print("Exiting...")
        return False

def loading(percent):
    print("\u001b[1A\u001b[0KLoading: " + str(percent) + "%")

if __name__ == '__main__':
    try:
        while True:
            email = input("Enter email: ")
            password = input("Enter password: ")
            password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
            loggedin = login(email, password)
            try:
                successLogin = loggedin['login_success']
            except:
                successLogin = False
            if successLogin:
                print()
                print("Logged in successfully")
                print()
                
                data = get_question()
                maxlimit = data['manual_verification']['max_limit']
                limit_used = data['manual_verification']['limit_used']
                available_points = data['manual_verification']['available_points']
                ans = data['answer']
                limit = (maxlimit - limit_used) - available_points
                limit = available_points if limit > 0 else maxlimit - limit_used
                print("LIMIT: " + str(limit))
                limit_per_loop = 100
                last_loop = limit % limit_per_loop
                loops = (limit // limit_per_loop)
                loops = loops if (limit % limit_per_loop) == 0 else loops + 1
                for i in range(loops):
                    threads = []
                    limit_now = limit_per_loop if i < loops else last_loop
                    for j in range(limit_now):
                        try:
                            thread = threading.Thread(target=answer, args=(ans,))
                            thread.start()
                            threads.append(thread)
                        except:
                            break
                    completed = 0
                    print("Session " + str(i + 1))
                    print()
                    for thread in threads:
                        thread.join()
                        completed += 1
                        percent = (completed / limit_now) * 100
                        loading(int(percent))
                print("LATEST BALANCE: " + latest_balance)
                print("All tasks completed")
                if not tryagain():
                    break
            else:
                print("Login failed")
    except KeyboardInterrupt:
        print()
        print("Exiting...")
    except:
        print("An error occurred")
        print("Exiting...")
        
