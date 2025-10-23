# lxpanel-lsyncd-logtracker
Little tool to follow lsyncd progression.

This will show a small icon on the top bar of the UI.

## Usage
This tool is created to run on Linux, specially on a Raspberry Pi running Raspbian. 

### MacOS
1. Update the `volumes` section in the `docker-compose.yaml` file to point to the right folders:
    * `/path/to/source:/source`: change to point to the source folder. lsyncd will take files from there
    * `/path/to/target:/target`: change to point to the target folder. lsyncd will put files there
    * `/path/to/logs:/logs`: lsyncd will write logs there

2. Setup the project with the makefile: `make setup`

3. Run the project with the makefile: `make run`

To setup/run without the makefile, check the content of the `Makefile` to run the right commands.

### Linux/Raspbian

