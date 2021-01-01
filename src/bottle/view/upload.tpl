<!DOCTYPE html>
<html>
<head>
<title>Hello {{name}}</title>
</head>
<body>

<h1>Upload photos!</h1>
<p>Hello {{name}} :) How are you? Please select photos, you want to add to album:</p>

<form action="/upload" method="post" enctype="multipart/form-data">
  Select a file: <input type="file" name="upload" />
  <input type="submit" value="Start upload" />
</form>

</body>
</html>
