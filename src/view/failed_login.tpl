<!DOCTYPE html>
<html>
<head>
<title> Login failed</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
 rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8">
</head>


<body>
<div class = "container">
<br>
<b>{{msg}}</b>
<br>
<br>
<form action="/login" method="get">
    <input name = login value="Go back" type="submit" class="btn btn-danger"/>
</form>
</div>
</body>
</html>