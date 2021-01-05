<!DOCTYPE html>
<html lang="en">
<head>
<title>Gallery </title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
 rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8">

</head>
<body>
<div class = "container">
<h1>Gallery</h1>

<p>Hello, welcome to your gallery :)</p>

<form action="/" method="post">
    <input name = main_page value="Go to main page" type="submit" class="btn btn-outline-primary"/>
</form>
<br>
<form action="/gallery" method="post" enctype="multipart/form-data">
  Select a file to upload more pictures: <input type="file" name="upload" />
  <input class="form-control" type="submit" value="Start upload" />
</form>
<br>

<form action="/gallery" method="post">
  <label for="sort_gallery"><b>View pictures in this gallery sorted by:</b></label>
  <select id= sort_gallery name= sort_gallery>
    <option value="likes">Likes</option>
    <option value="dislikes">Dislikes</option>
    <option value="date">Uploade date</option>
    <option value="comments">Number of comments</option>
  </select>
    <select id= sort_gallery_reverse name= sort_gallery_reverse>
    <option value="reverse">Descending</option>
    <option value="nonreverse">Ascending</option>
  </select>
  <input type="submit" class="btn btn-outline-primary btn-sm">
</form>
<br>
% for image in images:
% image_name = f"{image['image_name']}{image['ext']}"
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
<div>
<img src="{{ get_url('database', filename= image_name) }}" class="img-fluid" />
</div>
<br>
<form action="/gallery" method="post">
<b>{{likes}}  </b> <input name = {{like_name}} value= "Like" type="submit" class="btn btn-success btn-sm"/>
<form action="/gallery" method="post">
<b>{{dislikes}} </b>  <input name = {{dislike_name}} value= "Disike" type="submit" class="btn btn-danger btn-sm" > 
<br><i>Uploaded at:</i> {{date}}

<b><br><br>Comments:</b>
% for comment in image["comments"]:
<li>{{comment}}
</li>
%end
<br>
<form action="/gallery" method="post">
    Comment: <input name="{{comment_name}}" type="text" placeholder= "I like this picture." aria-label="default input example"/>
    <input value="Add comment" type="submit" class="btn btn-outline-primary btn-sm"/>
</form>

<br><b>Filter this image &amp add it to your gallery:</b>

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
  <input type="submit" class="btn btn-outline-primary btn-sm">
</form>
</ul>
%end
</form>

<br>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js"
 integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script
</body>
</html>
