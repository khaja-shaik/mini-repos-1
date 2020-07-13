## Purpose
* Script to find duplicate files in a folder.
* `dups` folder contains the files where duplicates have to searched for.
* To run the script manually, use command `python find_duplicates.py <path_to_directory>`

## Command to build docker image
`docker build -t list-dup --build-arg directory_path='dups' .
`
## Command to run the container
`docker run list-dup`

## Create job
`kubectl apply -f job.yml`
