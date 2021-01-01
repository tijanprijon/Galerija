<!DOCTYPE html>
<html>
<head>
<title>Hello {{name}}</title>
</head>
<body>
<b>Already have an account? Login</b> :
<form action="/login" method="post">
    Username: <input name="username" type="text" />
    Password: <input name="password" type="password" />
    <input value="Login" type="submit" />
</form>
<b>First time? Sign in:</b>
<form action="/login" method="post">
    New username: <input name="new_username" type="text" />
    New password: <input name="new_password" type="password" />
    <input value="Sign in" type="submit" />
</form>
</body>
</html>