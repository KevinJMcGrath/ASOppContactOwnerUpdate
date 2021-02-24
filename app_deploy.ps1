# https://devcenter.heroku.com/articles/container-registry-and-runtime
 #>

# log in to heroku
heroku login

# create dyno/instance/whatever
heroku create


# change stack to container for docker deploy
heroku stack:set container

# log in to container registry
heroku container:login

# The above commands we only do the first time then we can deploy as much we like


# "worker" is the process type. Still not 100% clear on what options are avaiable or what they mean contextually
heroku container:push worker

# create a "release"
heroku container:release worker


# Post install maintenance commands



# check the logs
# https://devcenter.heroku.com/articles/logging
heroku logs -a <app name>
heroku logs -a <app name> -n 200
heroku logs -a <app name> --tail

# list apps
heroku apps

# restart dyno
heroku dyno:restart -a powerful-tundra-96461
