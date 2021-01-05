<!DOCTYPE html>
<html>
<head>
<title>Login {{name}}</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
 rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8">
</head>


<body>
<h1>Login</h1>
<br>
<p><b>Already have an account? Login:</b></p>
<form action="/login" method="post">
    Username: <input name="username" type="text" placeholder= "Username" class="btn btn-outline-primary btn-sm" />
    Password: <input name="password" type="password" placeholder= "12345678"  class="btn btn-outline-primary btn-sm"/>
    <input value="Login" type="submit" class="btn btn-outline-success btn-sm"/>
</form>
<br>
<p><b>First time? Sign in:</b></p>
<form action="/login" method="post">
    New username: <input name="new_username" type="text" placeholder= "User123"  class="btn btn-outline-primary btn-sm"/>
    New password: <input name="new_password" type="password" placeholder= "Password123" class="btn btn-outline-primary btn-sm"/>
    <input value="Sign in" type="submit"class="btn btn-outline-success btn-sm"  />
</form>
</body>
</html>