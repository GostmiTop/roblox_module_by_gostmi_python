import requests
from re import findall

def cookie_fresher(filenamewithcookie):
    class Bypass:
        def __init__(self, cookie) -> None:
            self.cookie = cookie

        def start_process(self):
            self.xcsrf_token = self.get_csrf_token()
            self.rbx_authentication_ticket = self.get_rbx_authentication_ticket()
            return self.get_set_cookie()

        def get_set_cookie(self):
            response = requests.post(
                "https://auth.roblox.com/v1/authentication-ticket/redeem",
                headers={"rbxauthenticationnegotiation": "1"},
                json={"authenticationTicket": self.rbx_authentication_ticket}
            )
            set_cookie_header = response.headers.get("set-cookie")
            if not set_cookie_header:
                return "Invalid Cookie"

            valid_cookie = set_cookie_header.split(".ROBLOSECURITY=")[1].split(";")[0]
            return f"{valid_cookie}"

        def get_rbx_authentication_ticket(self):
            response = requests.post(
                "https://auth.roblox.com/v1/authentication-ticket",
                headers={
                    "rbxauthenticationnegotiation": "1",
                    "referer": "https://www.roblox.com/camel",
                    "Content-Type": "application/json",
                    "x-csrf-token": self.xcsrf_token
                },
                cookies={".ROBLOSECURITY": self.cookie}
            )
            assert response.headers.get(
                "rbx-authentication-ticket"), "An error occurred while getting the rbx-authentication-ticket"
            return response.headers.get("rbx-authentication-ticket")

        def get_csrf_token(self) -> str:
            response = requests.post("https://auth.roblox.com/v2/logout", cookies={".ROBLOSECURITY": self.cookie})
            xcsrf_token = response.headers.get("x-csrf-token")
            assert xcsrf_token, "An error occurred while getting the X-CSRF-TOKEN. Could be due to an invalid Roblox Cookie"
            return xcsrf_token

    def install_pyperclip():
        try:
            import pyperclip
        except ImportError:
            print("Module 'pyperclip' not found. Loading installation...")
            import subprocess
            subprocess.check_call(["python", "-m", "pip", "install", "pyperclip"])
            print("Installation successful")

    def main():
        install_pyperclip()
        import pyperclip
        try:
            with open(filenamewithcookie, "r") as infile:
                cookies = infile.readlines()
        except FileNotFoundError:
            print("file with cookie not found.")
            return

        refreshed_cookies = []

        for cookie in cookies:
            cookie = cookie.strip()
            if not cookie:
                continue
            bypass = Bypass(cookie)
            try:
                result = bypass.start_process()
                if not result.startswith("Invalid Cookie"):
                    refreshed_cookies.append(result)
            except Exception as e:
                print(f"Error processing cookie {cookie}: {e}")

        if refreshed_cookies:
            try:
                with open("Refreshed cookies.txt", "w") as outfile:
                    for refreshed_cookie in refreshed_cookies:
                        outfile.write(refreshed_cookie + "\n")
                print("Refreshed cookies written to Refreshed cookies.txt.")
            except Exception as e:
                print(f"Error writing to Refreshed cookies.txt: {e}")
        else:
            print("No valid cookies found.")

    if __name__ == "__main__":
        main()

def valid_cookie_check(cookie):
    check = requests.get('https://economy.roblox.com/v1/user/currency', cookies={'.ROBLOSECURITY': cookie})
    if check.status_code == 200:
        return "valid"
    else:
        return 'invalid'

class account:
    def get_user_id(cookie):
        userinfo = requests.get("https://www.roblox.com/my/settings/json", cookies={".ROBLOSECURITY": cookie}).json()
        userid = userinfo["UserId"]
        return userid

    def get_balance(cookie, userid):
        robux = requests.get(f'https://economy.roblox.com/v1/users/{userid}/currency', cookies={'.ROBLOSECURITY': cookie}).json()['robux']
        return robux

    def get_billing(cookie, userid):
        balance_creit_info = requests.get(f'https://billing.roblox.com/v1/credit', cookies={'.ROBLOSECURITY': cookie})
        balance_credit = balance_creit_info.json()['balance']
        balance_credit_currency = balance_creit_info.json()['currencyCode']
        billing = str(balance_credit) + " " + str(balance_credit_currency)
        return billing

    def get_rap(cookie, userid):
        rap_dict = requests.get(f'https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?assetType=All&sortOrder=Asc&limit=100', cookies={".ROBLOSECURITY": cookie}).json()
        while rap_dict['nextPageCursor'] != None:
            rap_dict = requests.get(f'https://inventory.roblox.com/v1/users/{userid}/assets/collectibles?assetType=All&sortOrder=Asc&limit=100', cookies={".ROBLOSECURITY": cookie}).json()
        rap = sum(i['recentAveragePrice'] for i in rap_dict['data'])
        return rap

    def get_account_sales_of_goods(cookie, userid):
        account_transactions = requests.get(f'https://economy.roblox.com/v2/users/{userid}/transaction-totals?timeFrame=Year&transactionType=summary',cookies={'.ROBLOSECURITY': cookie}).json()
        account_sales_of_goods = account_transactions['salesTotal']
        return account_sales_of_goods

    def get_account_donate(cookie, userid):
        account_transactions = requests.get(f'https://economy.roblox.com/v2/users/{userid}/transaction-totals?timeFrame=Year&transactionType=summary',cookies={'.ROBLOSECURITY': cookie}).json()
        donate = account_transactions['outgoingRobuxTotal']
        donate = str(donate).replace('-', '')
        return donate

    def get_premium(cookie, userid):
        account_transactions = requests.get(f'https://economy.roblox.com/v2/users/{userid}/transaction-totals?timeFrame=Year&transactionType=summary',cookies={'.ROBLOSECURITY': cookie}).json()
        account_sales_of_goods = account_transactions['salesTotal']
        return account_sales_of_goods

    def get_voice_chat(cookie):
        voice_chat = requests.get('https://voice.roblox.com/v1/settings', cookies={'.ROBLOSECURITY': cookie}).json()['isVerifiedForVoice']
        return voice_chat

    def get_gamepass_worth(cookie, userid):
        all_gamepasses = requests.get(f'https://www.roblox.com/users/inventory/list-json?assetTypeId=34&cursor=&itemsPerPage=100&pageNumber=1&userId={userid}', cookies={'.ROBLOSECURITY': cookie})
        check = findall(r'"PriceInRobux":(.*?),', all_gamepasses.text)
        account_gamepasses = str(sum([int(match) if match != "null" else 0 for match in check])) + f' R$'
        return account_gamepasses

    def get_email_verified(cookie):
        account_settings = requests.get(f'https://www.roblox.com/my/settings/json', cookies={'.ROBLOSECURITY': cookie})
        email = account_settings.json()['IsEmailVerified']
        return email

    def get_account_above_13(cookie):
        account_settings = requests.get(f'https://www.roblox.com/my/settings/json', cookies={'.ROBLOSECURITY': cookie})
        account_above_13 = account_settings.json()['UserAbove13']
        return account_above_13

    def get_account_age(cookie):
        account_settings = requests.get(f'https://www.roblox.com/my/settings/json', cookies={'.ROBLOSECURITY': cookie})
        account_age= round(float(account_settings / 365), 2)
        return str(account_age) + str(" years")

    def get_has_pin(cookie):
        account_settings = requests.get(f'https://www.roblox.com/my/settings/json', cookies={'.ROBLOSECURITY': cookie})
        account_has_pin = account_settings.json()['IsAccountPinEnabled']
        return account_has_pin

    def get_has_2fa(cookie):
        account_settings = requests.get(f'https://www.roblox.com/my/settings/json', cookies={'.ROBLOSECURITY': cookie})
        account_2fa = account_settings.json()['MyAccountSecurityModel']['IsTwoStepEnabled']
        return account_2fa

    def get_description(cookie):
        description = requests.get(f'https://users.roblox.com/v1/description', cookies={'.ROBLOSECURITY': cookie}).json()['description']
        return description

    def get_friends_count(cookie):
        friends = requests.get("https://friends.roblox.com/v1/my/friends/count", cookies={".ROBLOSECURITY": cookie}).json()["count"]
        return friends

    def get_account_url(cookie_or_userid):
        if cookie_or_userid.isdigit():
            url = "https://www.roblox.com/users/" + str(cookie_or_userid) + "/profile"
        else:
            userinfo = requests.get("https://www.roblox.com/my/settings/json", cookies={".ROBLOSECURITY": cookie_or_userid}).json()
            userid = userinfo["UserId"]
            url = "https://www.roblox.com/users/" + str(userid) + "/profile"
        return url

    def get_account_county_code(cookie):
        req = requests.get('https://users.roblox.com/v1/users/authenticated/country-code', cookies={".ROBLOSECURITY": cookie}).json()['countryCode']
        return req

    def get_username(cookie):
        req = requests.get('https://users.roblox.com/v1/users/authenticated', cookies={".ROBLOSECURITY": cookie}).json()['name']
        return req

    def get_displayname(cookie):
        req = requests.get('https://users.roblox.com/v1/users/authenticated', cookies={".ROBLOSECURITY": cookie}).json()['displayName']
        return req

    def get_account_creation_date(cookie, userid):
        req = requests.get(f'https://users.roblox.com/v1/users/{userid}', cookies={".ROBLOSECURITY": cookie}).json()['created']
        return req

    def get_thumbnail_url(cookie):
        req = requests.get('https://www.roblox.com/mobileapi/userinfo', cookies={".ROBLOSECURITY": cookie}).json()['ThumbnailUrl']
        return req

    def get_how_many_friends(cookie):
        req = requests.get('https://friends.roblox.com/v1/my/friends/count', cookies={".ROBLOSECURITY": cookie}).json()['count']
        return req

    def get_how_many_followers(cookie, userid):
        req = requests.get(f'https://friends.roblox.com/v1/users/{userid}/followers/count', cookies={".ROBLOSECURITY": cookie}).json()['count']
        return req

    def get_friends_requests_count(cookie):
        req = requests.get('https://friends.roblox.com/v1/user/friend-requests/count', cookies={".ROBLOSECURITY": cookie}).json()['count']
        return req

    def badge_check(badges_ids, userid):
        badgefile = str(badges_ids).split(',')
        if len(badgefile) >= 1:
            havebd = []
            lenght = len(badgefile)
            while lenght >= 1:
                firstel = badgefile[0]
                badgefile.pop(0)
                req = requests.get(f'https://inventory.roblox.com/v1/users/{userid}/items/2/{firstel}/is-owned')
                if req.text == "true":
                    havebd.append(firstel)
                lenght -= 1
                lenght = len(badgefile)
        else:
            havebd = 'null'
            print('Вы не указали badges_ids.Например: 87858345,374576345,7346576345 и т.д')
        if len(havebd) < 1:
            havebd = 'null'
        return havebd

    def gamepass_check(gamepasses_ids, userid):
        gamepassfile = str(gamepasses_ids).split(',')
        if len(gamepassfile) >= 1:
            havegp = []
            lenght = len(gamepassfile)
            while lenght >= 1:
                firstel = gamepassfile[0]
                gamepassfile.pop(0)
                req = requests.get(f'https://inventory.roblox.com/v1/users/{userid}/items/1/{firstel}/is-owned')
                if req.text == 'true':
                    havegp.append(firstel)
                lenght -= 1
                lenght = len(gamepassfile)
        else:
            havegp = 'null'
            print('Вы не указали gamepasses_ids.Например: 87858345,374576345,7346576345 и т.д')
        if len(havegp) < 1:
            havegp = 'null'
        return havegp

    def get_how_many_trade_requests(cookie):
        req = requests.get('https://trades.roblox.com/v1/trades/inbound/count', cookies={".ROBLOSECURITY": cookie}).json()['count']
        return req

    def get_user_last_online(cookie, userid):
        data = {
            "userIds":[userid],
            "Content-Type":'application/json;charset=utf-8'
        }
        req = requests.post('https://presence.roblox.com/v1/presence/users', cookies={".ROBLOSECURITY": cookie}, json=data).json()['userPresences']
        req = str(req).split("'lastOnline': ")
        req = str(req[1]).split('}]"')
        req = str(req[0]).split('}]')[0]
        req = req.replace("'", '')
        return req

    def get_phone_verify(cookie):
        req = requests.get('https://accountinformation.roblox.com/v1/phone',cookies={".ROBLOSECURITY": cookie}).json()['isVerified']
        return req

    def get_promotion_channels(cookie):
        req = requests.get('https://accountinformation.roblox.com/v1/promotion-channels?alwaysReturnUrls=false&filterLink=false',cookies={".ROBLOSECURITY": cookie}).json()
        return req

    def get_star_code(cookie):
        req = requests.get('https://accountinformation.roblox.com/v1/star-code-affiliates',cookies={".ROBLOSECURITY": cookie}).text
        return req

    def get_roblox_badges(cookie, userid):
        req = requests.get(f'https://accountinformation.roblox.com/v1/users/{userid}/roblox-badges', cookies={".ROBLOSECURITY": cookie}).json()
        badges = []
        for items in req:
            badges.append(items.get('name'))
        return badges

class groups:
    def get_account_groups(userid, cookie):
        all_groups = requests.get(f'https://groups.roblox.com/v2/users/{userid}/groups/roles?includeLocked=false&includeNotificationPreferences=false', cookies={".ROBLOSECURITY": cookie}).json()
        return all_groups

    def check_account_in_group(cookie, userid, groups_ids):
        all_groups = requests.get(f'https://groups.roblox.com/v2/users/{userid}/groups/roles?includeLocked=false&includeNotificationPreferences=false', cookies={".ROBLOSECURITY": cookie}).text
        in_group = []
        groups_ids = str(groups_ids).split(',')
        if len(groups_ids) >= 1:
            lenght = len(groups_ids)
            while lenght >= 1:
                firstel = groups_ids[0]
                groups_ids.pop(0)
                if str(firstel) in str(all_groups):
                    in_group.append(firstel)
                lenght -= 1
                lenght = len(groups_ids)
        else:
            print('Вы не указали айди груп для проверки(например: 657346753,7346576345 и т.д):/')
        if len(in_group) < 1:
            in_group = '-'
        return in_group

    def get_own_groups(cookie, userid):
        req = requests.get(f'https://groups.roblox.com/v1/users/{userid}/groups/primary/role', cookies={".ROBLOSECURITY": cookie}).json()
        if req == 'None':
            return req
        else:
            req = req["group"]['id']
            return req

    def get_balance_by_id_group(cookie, group_id):
        req = requests.get(f'https://economy.roblox.com/v1/groups/{group_id}/currency', cookies={".ROBLOSECURITY": cookie}).json()['robux']
        return req
