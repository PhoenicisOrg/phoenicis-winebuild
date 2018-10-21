# phoenicis-winebuild

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5a2ba048397a4c3dac18682b6045b9c6)](https://app.codacy.com/app/PhoenicisOrg/phoenicis-winebuild?utm_source=github.com&utm_medium=referral&utm_content=PhoenicisOrg/phoenicis-winebuild&utm_campaign=Badge_Grade_Dashboard)

Phoenicis Winebuild is a python library and a command line tool that compiles winehq automatically. It is the designated successor of PlayOnLinux Winebuild service.

Phoenicis Winebuild can:
  - run on any OS (Linux and Mac OS)
  - build wine for any target OS (see prerequisites).

## Prerequisites
  - Python 3
  - Docker
  - docker-py

    pip install docker

### Linux user
Ensure that your current user belongs to the docker group. You might need to restart your session

### OSX targeted builds
You need to extract Mac OS 10.8 SDK from XCode 4, compress it into a .tar.xz file and place it to darwin/SDK directory  




## How to use
### Basic usage
After setup, run examples/interactive_builder.py
   PYTHONPATH="$PWD" python examples/interactive_builder.py  

### Key concepts
#### Environment
An *Environment* is a pre-installed operating system where wine can be built. It corresponds to a docker image. We support currently two environment:

  - **linux-x86-wine** is a x86 environment containing all tools required to build wine for Linux
  - **darwin-x86-wine** is a x86 environment containing all tools required to cross-compile wine for MacOS

#### Container
A container is the instanciation of an environment. It corresponds to a docker container. Thanks to containers, you can run multiple compilation inside a given environment at the same time

#### Builders
A *Builder* is the components that builds wine. A builder needs a container to operate. We currently support one kind of builder :

  - **WineBuilder** downloads the source of wine into /root/wine-git and runs a script

#### Script
A script can be run inside a context initiated by a builder. We have two scripts:
  - builder_darwin_x86_wine
  - builder_linux_x86_wine

### Web Services
After setup, run run_web_server.py

#### Create an environment
 * Go to the endpoint /environments (http://localhost:5000/environments)
 * Grab the docker name of a supported environment (exemple: phoenicis/winebuild/linux-x86:wine)
 * Create an environement creation task

    curl -d '{"type": "EnvironmentCreationTask", "argument": "phoenicis/winebuild/linux-x86:wine"}' -H "Content-Type: application/json" -X POST http://localhost:5000/tasks

 * Go to the endpoint /tasks to track the task creation process: http://127.0.0.1:5000/tasks. You should get a response like this one:

 [{
   "argument": {
     "docker_name": "phoenicis/winebuild/linux-x86:wine_osxcross"
   },
   "description": "Environment creation: phoenicis/winebuild/linux-x86:wine_osxcross",
   "end_date": null,
   "id": "698ed9bd-f0af-4ed4-9063-d058fb7ec391",
   "last_update_date": "Sun, 21 Oct 2018 14:22:51 GMT",
   "progress": 94,
   "running": true,
   "start_date": "Sun, 21 Oct 2018 14:18:39 GMT",
   "type": "EnvironmentCreationTask"
  }]

### Advanced scripting
You have two example python files (example_linux.py and example_darwin.py). If you need to tweak your build (select the version, use custom script, ...) you'll probably need to use the python API (See Key Concepts)

#### Examples
    #!/usr/bin/env python
    from core.Container import Container
    from core.Environment import Environment
    from builders.WineBuilder import WineBuilder

    ## Creates an environment that is suitable to compile darwin-x86 versiuon of wine
    environment = Environment("wine", "darwin", "x86")
    ## Build the environment
    environment.build()

    ## Starts a new container inside our environment
    container = Container(environment)
    container.start()

    ## Creates a builder inside our container
    builder = WineBuilder(container)

    ## Builds wine 3.0.3 with the script builders/builder_darwin_x86_wine
    builder.build("builders/builder_darwin_x86_wine", "wine-3.0.3")

    ## Archive the compiled binaries into wine-3.0.3-darwin.tar.gz
    builder.archive("wine-3.0.3-darwin.tar.gz")

## Running wine
### On OSX
The dependencies are bundled into the output archive by default.
You have to set environment variables so that wine can find its dependencies.

    export FREETYPE_PROPERTIES="truetype:interpreter-version=35"
    export DYLD_FALLBACK_LIBRARY_PATH="$PWD/../lib/"
    ./wine winecfg

## TODO
  - Webservice system
  - 64bits support
