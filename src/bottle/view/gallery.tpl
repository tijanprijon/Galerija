<!DOCTYPE html>
<html>
<head>
<title>Hello </title>
</head>
<body>

<h1>Gallery</h1>
<p>Hello, welcome to your gallery :)</p>

<form action="/" method="post">
    <input name = main_page value="Go to main page" type="submit" />
</form>
<br>
<form action="/gallery" method="post" enctype="multipart/form-data">
  Select a file to upload more pictures: <input type="file" name="upload" />
  <input type="submit" value="Start upload" />
</form>

% for image in images:
% image_name = f"images/{image['image_name']}{image['ext']}"
% likes = f'{image["likes"]}' +  " likes"
% like_name = f'like_{image["image_name"]}'
% dislike_name = f'dislike_{image["image_name"]}'
% comment_name = f'comment_{image["image_name"]}'
% filter_name = f'filter_{image["image_name"]}'
% if likes == "1 likes":
% likes = "1 like"
%end
% dislikes = f'{image["dislikes"]}' +  " dislikes"
% if dislikes == "1 dislikes":
% dislikes = "1 dislike"
%end
%date = image["date"]
<ul>
<img src="{{ get_url('static', filename= image_name) }}"/>

<form action="/gallery" method="post">
{{likes}}   <input name = {{like_name}} value= "Like" type="submit" />
<form action="/gallery" method="post">
{{dislikes}}   <input name = {{dislike_name}} value= "Disike" type="submit" />
<br>Uploaded at: {{date}}

<b><br><br>Comments:</b>
% for comment in image["comments"]:
<li>{{comment}}
</li>
%end
<br>
<form action="/gallery" method="post">
    Comment: <input name="{{comment_name}}" type="text" />
    <input value="Add comment" type="submit" />
</form>

<br>Filter this image &amp add it to your gallery:

<form action="/gallery" method="post">
  <label for="filter">Choose a filter:</label>
  <select id= {{filter_name}} name= {{filter_name}}>
    <option value="BLUR">Blur</option>
    <option value="EMBOSS">Emboss</option>
    <option value="EDGE_ENHANCE">Edge enhancement</option>
    <option value="EDGE_ENHANCE_MORE">More edge enhancement</option>
    <option value="CONTOUR">Contour</option>
    <option value="GRAYSCALE">Grayscale</option>
  </select>
  <input type="submit">

</form>

</ul>
%end

</form>
</body>
</html>
