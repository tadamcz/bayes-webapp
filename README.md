* Do a Bayesian update where the prior PDF and the likelihood function are continuous. Currently supports 1 dimensional distributions. 
* Web application for the library [tadamcz/bayes-continuous](https://github.com/tadamcz/bayes-continuous).
* Deployed at [bayesupdate.com/](https://bayesupdate.com/)

# Screenshot
[![Alt text](Capture.PNG "Optional title")](https://bayesupdate.com/)

# Development
[tadamcz/bayes-continuous](https://github.com/tadamcz/bayes-continuous) is used as a git submodule (see `.gitmodules`). You'll need to initialized and update that submodule. It's easiest to do this initially by passing `--recurse-submodules` to the `git clone` command. 

# Deployment
Uses Dokku. Dokku expects the file `.buildpacks`.
