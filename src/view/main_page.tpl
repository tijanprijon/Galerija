<!DOCTYPE html>
<html>
<head>
<title>Hello {{name}}</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
 rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8">
</head>
<body>
<div class = "container">
<h1>MAIN PAGE</h1>
<br>
<p>Hello <b>{{name}}</b> :) How are you?</p>
<form action="/" method="post">
    <input name = login value="Login / create account" type="submit" class="btn btn-outline-success btn-lg"/>
</form>
<br>
<form action="/" method="post">
    <input name = gallery value="View gallery" type="submit" class="btn btn-outline-primary btn-lg" />
</form>

</div>
</body>
</html>
