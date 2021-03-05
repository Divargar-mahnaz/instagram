DAYS_OF_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
WEBSITE_PATTERN = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
PASSWORD_PATTERN = "^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#/$])[\w\d@/#$]{6,}$"
PHONE_PATTERN = '^(09[0-9]{9})$'
EMAIL_PATTERN = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
USERNAME_PATTERN = '^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$'
